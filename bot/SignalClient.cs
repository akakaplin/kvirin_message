using libsignalservice;
using libsignalservice.push.exceptions;
using libsignalservice.websocket;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Security;
using System.Net.WebSockets;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Sample {
	public class NetCoreSignalSocketFactory : ISignalWebSocketFactory {
        public ISignalWebSocket CreateSignalWebSocket(Uri uri, CancellationToken? token = null)
        {
			return new NetCoreSignalWebSocket(token ?? default, uri);
		}
    }

	public class NetCoreSignalWebSocket : ISignalWebSocket {
		private ClientWebSocket WebSocket;
		private readonly ILogger Logger = LibsignalLogging.CreateLogger<NetCoreSignalWebSocket>();
		private readonly SemaphoreSlim SemaphoreSlim = new SemaphoreSlim(1, 1);
		private readonly Uri SignalWSUri;
		private readonly CancellationToken Token;
#pragma warning disable CS0067 //
		public event EventHandler<SignalWebSocketClosedEventArgs> Closed;
#pragma warning restore CS0067 // 
		public event EventHandler<SignalWebSocketMessageReceivedEventArgs> MessageReceived;

		public NetCoreSignalWebSocket(CancellationToken token, Uri uri) {
			Connecting = new TaskCompletionSource<bool>();
			CreateMessageWebSocket();
			Token = token;
			SignalWSUri = uri;

			MessageReceivedLoop();
		}
		private bool RemoteCertificateValidationCallback(object sender, X509Certificate cert, X509Chain chain, SslPolicyErrors sslPolicyErrors) {
			if (sslPolicyErrors == SslPolicyErrors.None)
				return true;
			if (libsignalservice.util.Util.Certificate?.Length > 0)
				return cert.GetRawCertData().SequenceEqual(libsignalservice.util.Util.Certificate);
			return false;
		}
		private void CreateMessageWebSocket() {
			WebSocket = new ClientWebSocket();
			WebSocket.Options.KeepAliveInterval = TimeSpan.FromSeconds(30);
			WebSocket.Options.RemoteCertificateValidationCallback = RemoteCertificateValidationCallback;

		}


		private const int ReceiveChunkSize = 1024;
		//	
		private TaskCompletionSource<bool> Connecting;
		private async void MessageReceivedLoop() {
			var buffer = new byte[ReceiveChunkSize];
			while (!Token.IsCancellationRequested) {
				var tsk = Connecting?.Task;
				while (tsk != null) {
					if ((await tsk) == true)
						break;
					if (Token.IsCancellationRequested)
						return;
					tsk = Connecting?.Task;
				}
				var message = new MemoryStream();
				WebSocketReceiveResult result;
				try {
					do {
						result = await WebSocket.ReceiveAsync(new ArraySegment<byte>(buffer), Token);
						if (result.MessageType == WebSocketMessageType.Close) {
							await WebSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
							throw new Exception("Got a close message requesting reconnect");
						} else {
							message.Write(buffer, 0, result.Count);
						}
					} while (!result.EndOfMessage);
					MessageReceived.Invoke(this, new SignalWebSocketMessageReceivedEventArgs { Message = message.ToArray() });
				} catch (TaskCanceledException) {
					Logger.LogDebug("HandleIncomingWS shutting down");
				} catch (Exception e) {
					if (!Token.IsCancellationRequested) {
						Logger.LogWarning("HandleIncomingWS recv failed ({0})", e.Message);
						Logger.LogInformation("HandleIncomingWS reconnecting");
						await Task.Run(ConnectAsync);
					}
				}
			}
		}

		public void Close(ushort code, string reason) {
			Logger.LogTrace("Closing SignalWebSocket connection");
			WebSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, reason, Token).Wait();

		}

		public async Task ConnectAsync() {
			Logger.LogTrace("ConnectAsync()");
			var locked = await SemaphoreSlim.WaitAsync(0, Token); // ensure no threads are reconnecting at the same time
			if (locked) {
#pragma warning disable CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed
				if (WebSocket != null) {
					var old_socket = WebSocket;
					Task.Run(() => { try { old_socket.CloseAsync(WebSocketCloseStatus.NormalClosure, "reconnecting", Token); } catch { } });
				}
#pragma warning restore CS4014 // Because this call is not awaited, execution of the current method continues before the call is completed
				while (!Token.IsCancellationRequested) {
					try {
						var old_tsk = Connecting;
						Connecting = new TaskCompletionSource<bool>();
						old_tsk.SetResult(false);
						CreateMessageWebSocket();
						Logger.LogTrace("WebSocket.ConnectAsync()");
						await WebSocket.ConnectAsync(SignalWSUri, Token);
						Connecting.SetResult(true);
						Connecting = null;
						SemaphoreSlim.Release();
						break;
					} catch (OperationCanceledException) { } catch (Exception e) {
						if (e.Message.Contains("(403)")) {
							SemaphoreSlim.Release();
							throw new AuthorizationFailedException("OWS server rejected authorization.");
						}
						Logger.LogError("ConnectAsync() failed: {0}\n{1}", e.Message, e.StackTrace); //System.Runtime.InteropServices.COMException (0x80072EE7)
						await Task.Delay(10 * 1000);
					}
				}
			} else {
				Logger.LogTrace("ConnectAsync() not reconnecting: Reconnect in progress");
			}
		}

		public void Dispose() {
			WebSocket.Dispose();
		}

		public async Task SendMessage(byte[] data) {
			Logger.LogTrace("SendMessage()");
			try {
				await WebSocket.SendAsync(data, WebSocketMessageType.Binary, true, CancellationToken.None);//none may be best we dont want to abort mid send as no retry option? dunnno same in main code
			} catch (OperationCanceledException) {
				Logger.LogTrace($"SendMessage() was cancelled");
			} catch (Exception e) {
				Logger.LogError($"SendMessage() failed: {e.Message}\n{e.StackTrace}");

				var t = Task.Run(ConnectAsync);
			}
		}
	}
}