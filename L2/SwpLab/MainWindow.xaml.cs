using Microsoft.Speech.Recognition;
using Microsoft.Speech.Synthesis;
using System;
using System.Globalization;
using System.Windows;
using System.Windows.Media;

namespace SwpLab
{
    public partial class MainWindow : Window
    {
        static SpeechSynthesizer synthesizer;
        static SpeechRecognitionEngine engine;

        public MainWindow()
        {
            synthesizer = new SpeechSynthesizer();
            synthesizer.SetOutputToDefaultAudioDevice();
            synthesizer.Speak("Witaj w asystencie kalkulacyjnym!");

            CultureInfo cultureInfo = new CultureInfo("pl-PL");

            engine = new SpeechRecognitionEngine(cultureInfo);
            engine.SetInputToDefaultAudioDevice();
            engine.SpeechRecognized += recognized;

            Grammar grammar = new Grammar("grammar.xml", "rootRule")
            {
                Enabled = true
            };

            engine.LoadGrammar(grammar);
            engine.RecognizeAsync(RecognizeMode.Multiple);

            InitializeComponent();
        }



        private void recognized(object sender, RecognitionEventArgs e)
        {
            clearButtons();

            string txt = e.Result.Text;
            Console.Out.WriteLine(txt);

            float confidence = e.Result.Confidence;
            if (confidence < 0.75)
            {
                synthesizer.Speak("Możesz powtórzyć?");
            }
            else
            {
                bool operation_performed = false;

                int num_1 = Convert.ToInt32(e.Result.Semantics["first"].Value);
                int num_2 = Convert.ToInt32(e.Result.Semantics["second"].Value);
                string op = e.Result.Semantics["operation"].Value.ToString();

                float result = 0.0F;

                if (op == "plus" || op == "dodaj")
                {
                    result = num_1 + num_2;
                    txt_display.Text = num_1 + "+" + num_2 + " = " + result + "";

                    btn_add.Background = new SolidColorBrush(Colors.Green);
                    operation_performed = true;
                }
                else if (op == "minus" || op == "odejmij")
                {
                    result = num_1 - num_2;
                    txt_display.Text = num_1 + "-" + num_2 + " = " + result + "";

                    btn_substract.Background = new SolidColorBrush(Colors.Green);
                    operation_performed = true;
                }
                else if (op == "pomnóż" || op == "razy")
                {
                    result = num_1 * num_2;
                    txt_display.Text = num_1 + "x" + num_2 + " = " + result + "";

                    btn_multiply.Background = new SolidColorBrush(Colors.Green);
                }
                else if (op == "podzielić" || op == "dzielone")
                {
                    if (num_1 == 0)
                    {
                        synthesizer.Speak("Nie można dzielić przez zero.");
                        return;
                    }
                    else
                    {
                        result = num_1 / num_2;

                        txt_display.Text = num_1 + "/" + num_2 + " = " + result;

                        btn_divide.Background = new SolidColorBrush(Colors.Green);
                        operation_performed = true;
                    }
                }

                if (operation_performed)
                {
                    digitHighlight(num_1);
                    digitHighlight(num_2);
                    btn_equals.Background = new SolidColorBrush(Colors.Yellow);
                    synthesizer.Speak("Wynik to: " + result);
                }
            }
        }

        private void btn_clear_Click(object sender, RoutedEventArgs e)
        {
            clearButtons();
            txt_display.Text = "0";
        }

        private void digitHighlight(int number)
        {
            switch (number)
            {
                case 0:
                    btn_0.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 1:
                    btn_1.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 2:
                    btn_2.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 3:
                    btn_3.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 4:
                    btn_4.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 5:
                    btn_5.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 6:
                    btn_6.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 7:
                    btn_7.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 8:
                    btn_8.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
                case 9:
                    btn_9.Background = new SolidColorBrush(Colors.NavajoWhite);
                    break;
            }
        }

        private void clearButtons()
        {
            // Buttons - digits
            btn_0.Background = new SolidColorBrush(Colors.LightGray);
            btn_1.Background = new SolidColorBrush(Colors.LightGray);
            btn_2.Background = new SolidColorBrush(Colors.LightGray);
            btn_3.Background = new SolidColorBrush(Colors.LightGray);
            btn_4.Background = new SolidColorBrush(Colors.LightGray);
            btn_5.Background = new SolidColorBrush(Colors.LightGray);
            btn_6.Background = new SolidColorBrush(Colors.LightGray);
            btn_7.Background = new SolidColorBrush(Colors.LightGray);
            btn_8.Background = new SolidColorBrush(Colors.LightGray);
            btn_9.Background = new SolidColorBrush(Colors.LightGray);

            // Buttons - operations
            btn_add.Background = new SolidColorBrush(Colors.DarkGray);
            btn_substract.Background = new SolidColorBrush(Colors.DarkGray);
            btn_multiply.Background = new SolidColorBrush(Colors.DarkGray);
            btn_divide.Background = new SolidColorBrush(Colors.DarkGray);

            // Button - execute
            btn_equals.Background = new SolidColorBrush(Colors.DarkOrange);
        }
    }
}
