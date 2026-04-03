//Як гість, я хочу зареєструватись через email/пароль, щоб зберігати файли.
namespace UserRegistrationApp
{
    class Program
    {
        // Проста "база даних" у пам'яті
        static Dictionary<string, string> users = new Dictionary<string, string>();

        static void Main(string[] args)
        {
            Console.WriteLine("--- Реєстрація нового користувача ---");

            Console.Write("Введіть ваш Email: ");
            string email = Console.ReadLine();

            Console.Write("Введіть пароль: ");
            string password = Console.ReadLine();

            if (RegisterUser(email, password))
            {
                Console.WriteLine("\n[Успіх]: Ви успішно зареєструвалися!");
                Console.WriteLine($"Тепер ви можете зберігати файли для аккаунту: {email}");
            }
            else
            {
                Console.WriteLine("\n[Помилка]: Користувач з таким Email вже існує.");
            }
        }

        static bool RegisterUser(string email, string password)
        {
            if (users.ContainsKey(email))
            {
                return false;
            }

            users.Add(email, password);
            return true;
        }
    }
}
