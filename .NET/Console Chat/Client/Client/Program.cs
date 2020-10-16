using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace UDP_CHAT_CLIENT
{
    class Program
    {
        static int remotePort; // Порт для отправки сообщений
        static IPAddress ipAddress; // IP адрес сервера
        static Socket listeningSocket;

        static string userName;
        static string readLine;

        static bool isFirstTime = true;

        static void Main(string[] args)
        {
            //string IP = Dns.GetHostByName(Host).AddressList[0].ToString();

            Console.WriteLine("Client chat");
            //Console.Write("Увядзiце ip адрас атрымальніка: ");
            //ipAddress = IPAddress.Parse(Console.ReadLine());
            ipAddress = IPAddress.Parse("127.0.0.1");
            Console.Write("Увядзiце порт для адпраўлення паведамленняў: ");
            remotePort = Int32.Parse(Console.ReadLine());
           // userName = Console.ReadLine();
       
            Console.WriteLine("Каб змянiць порт, увядзiце каманду /new");
            Console.WriteLine();
            /*
            EndPoint remoteIp = new IPEndPoint(IPAddress.Any, 0);
            byte[] data2 = new byte[256];

            IPEndPoint remoteFullIp = remoteIp as IPEndPoint; // получаем данные о подключении
            */

            try
            {
                listeningSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
                Task listeningTask = new Task(Listen); // Создание потока
                listeningTask.Start();

                while (true)
                {
                    string message;

                    if (isFirstTime) //  для апавяшчэння аб первым уваходзе да таго, як карыстач што-небудь напіша.
                    {
                        InputValidation();
                        message = userName + ':';
                        isFirstTime = false;
                    }
                    else
                    {
                        readLine = Console.ReadLine();
                        //Console.Write("Вы: ");
                        message = userName + ": " + readLine;
                    }

                    if (readLine == "/new")
                    {
                        Console.Write("\nУвядзiце порт для адпраўлення паведамленняў: ");
                        remotePort = Int32.Parse(Console.ReadLine());
                    }
                    else
                    { 
                        byte[] data = Encoding.Unicode.GetBytes(message);

                        EndPoint remotePoint = new IPEndPoint(ipAddress, remotePort);
                        listeningSocket.SendTo(data, remotePoint);
                    }
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

        // Поток для приема подключений
        private static void Listen()
        {
            try
            {
                IPEndPoint localIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), 0); // Прослушиваем по адресу
                listeningSocket.Bind(localIP);

                while (true)
                {
                    StringBuilder builder = new StringBuilder();
                    int bytes = 0;
                    byte[] data = new byte[256];

                    EndPoint remoteIp = new IPEndPoint(IPAddress.Any, 0);

                    do
                    {
                        bytes = listeningSocket.ReceiveFrom(data, ref remoteIp);
                        builder.Append(Encoding.Unicode.GetString(data, 0, bytes));
                    }
                    while (listeningSocket.Available > 0); // пакуль ёсць што браць з плыні

                    IPEndPoint remoteFullIp = remoteIp as IPEndPoint;

                    //Console.WriteLine("{0}, {1}", remoteFullIp.Port, remotePort);

                    /*
                    if (remoteFullIp.Port == remotePort)
                        Console.WriteLine("(GROUP CHAT), {0}", builder.ToString());
                    else
                        Console.WriteLine("(PERSONAL MESSAGE), ({0}), {1}", remoteFullIp.Port, builder.ToString());
                    */

                    if (builder[0] == '(')
                        Console.WriteLine("{0}", builder.ToString());
                    else if(builder[0] == '/')
                    {
                        Console.WriteLine(builder.ToString());
                    }
                    else
                    { 
                        Console.WriteLine("({0}) (Толькi Вам) {1} ({2})", remoteFullIp.Port, builder.ToString(), DateTime.Now.ToString("HH:mm:ss"));
                        RecievedMessage(remoteFullIp);
                    }
                    //Console.WriteLine("{2}", remoteFullIp.Address.ToString(), remoteFullIp.Port, builder.ToString());
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

        private static void RecievedMessage(EndPoint sender)
        {
            byte[] receivedMessageData = Encoding.Unicode.GetBytes("//(received)");
            listeningSocket.SendTo(receivedMessageData, sender);
        }

        private static void InputValidation()
        {
            while (true)
            {
                Console.Write("Увядзiце iмя: ");
                userName = Console.ReadLine();
                bool isInvalid = false;
                foreach (char symbol in userName)
                {
                    if (symbol == ' ' || symbol == ':' || symbol == '/' || userName == "")
                        isInvalid = true;
                }
                if (isInvalid)
                    Console.WriteLine("Недазволены фармат iмя. Паспрабуйце яшчэ раз");
                else
                    break;
            }
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