using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace UDP_CHAT_SERVER
{
    class Program
    {
        static int localPort; 
        static Socket listeningSocket;

        static List<IPEndPoint> clients = new List<IPEndPoint>();
        static string name;

        static void Main(string[] args)
        {
            Console.WriteLine("Main Statistics");
            Console.Write("Увядзiце порт для прыёму паведамленняў: ");
            localPort = Int32.Parse(Console.ReadLine());
            Console.WriteLine();

            try
            {
                listeningSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp); // Создание UDP сокета
                Task listeningTask = new Task(Listen);
                listeningTask.Start();
                listeningTask.Wait(); // Не идем дальше пока поток не будет остановлен
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                Close(); 
            }
        }

        // поток для приема подключений
        private static void Listen()
        {
            try
            {
                //Прослушиваем по адресу
                IPEndPoint localIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), localPort);
                listeningSocket.Bind(localIP);

                while (true)
                {
                    StringBuilder builder = new StringBuilder(); 
                    int bytes = 0; 
                    byte[] data = new byte[256];
                    EndPoint remoteIp = new IPEndPoint(IPAddress.Any, 0); //адрес, с которого пришли данные
                    do
                    {
                        bytes = listeningSocket.ReceiveFrom(data, ref remoteIp);
                        builder.Append(Encoding.Unicode.GetString(data, 0, bytes));
                    }
                    while (listeningSocket.Available > 0);

                    IPEndPoint remoteFullIp = remoteIp as IPEndPoint; // получаем данные о подключении

                    bool addClient = true;
                    for (int i = 0; i < clients.Count; i++)
                        if (clients[i].Port.ToString() == remoteFullIp.Port.ToString())
                            addClient = false;

                    if (addClient == true)
                    {
                        clients.Add(remoteFullIp);
                        name = GetName(builder);
                        Console.WriteLine("({0}:{1}) Карыстач {2} далучыўся", remoteFullIp.Address.ToString(), remoteFullIp.Port, name);
                        LoginMessage(name, remoteFullIp.Address.ToString(), remoteFullIp.Port.ToString());
                    }
                    else
                    {
                        Console.WriteLine("({0}:{1}) {2} ({3})", remoteFullIp.Address.ToString(), remoteFullIp.Port, builder.ToString(), DateTime.Now.ToString("HH:mm:ss"));
                        BroadcastMessage(builder.ToString(), remoteFullIp.Port.ToString());
                    }
                    // Console.WriteLine("Ваш порт: {0}", remoteFullIp.Port);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
            finally
            {
                Close();
            }
        }

        private static string GetName(StringBuilder builder)
        {
            string answer = "";
            for (int i = 0; i < builder.Length; i++)
            {
                if (builder[i] == ':')
                    return answer;
                answer += builder[i];
            }
            return "error";
        }


        private static void BroadcastMessage(string message, string port)
        {
            byte[] data = Encoding.Unicode.GetBytes("("+port+") " + message + " (" + DateTime.Now.ToString("HH:mm:ss") + ")"); // Формируем байты из текста
            byte[] receivedMessageData = Encoding.Unicode.GetBytes("    (received)"); 


            for (int i = 0; i < clients.Count; i++) 
                if (clients[i].Port.ToString() != port) 
                    listeningSocket.SendTo(data, clients[i]);
               // else if (clients[i].Port.ToString() == port && clients.Count > 1)
                    //listeningSocket.SendTo(receivedMessageData, clients[i]);
        }

        private static void LoginMessage(string name, string ip , string port)
        {
            byte[] data = Encoding.Unicode.GetBytes("("+ip+":"+port+") Карыстач " + name +  " далучыўся"); // Формируем байты из текста

            for (int i = 0; i < clients.Count; i++)
                //if (clients[i].Port.ToString() != port)
                    listeningSocket.SendTo(data, clients[i]);
        }

        private static void Close()
        {
            if (listeningSocket != null)
            {
                listeningSocket.Shutdown(SocketShutdown.Both);
                listeningSocket.Close();
                listeningSocket = null;
            }

            Console.WriteLine("Сервер спынены!");
        }
    }
}