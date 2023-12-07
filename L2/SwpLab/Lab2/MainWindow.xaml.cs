using System.Data;
using System.Windows;
using System.Windows.Media;
using System.Text.RegularExpressions;
using Humanizer;
using NAudio.CoreAudioApi;
using Microsoft.Speech.Synthesis;
using Microsoft.Speech.Recognition;

namespace Lab2
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private readonly Choices words;
        
        private readonly DataTable dataTable;
        private readonly MMDeviceEnumerator enumerator;

        private readonly SpeechRecognitionEngine recognizer;
        private readonly SpeechSynthesizer speechSynthesizer;

        private readonly GrammarBuilder? grammarBuilder;
        private readonly Grammar? grammar;

        public MainWindow()
        {
            InitializeComponent();

            recognizer = new SpeechRecognitionEngine();
            words = new Choices("0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "plus", "dodać", "dodaj", "razy", "pomnóż", "mnożyć", "podziel", "podzielić",
                "przez", "dziel", "odjąć", "odejmij", "minus", "wykonaj", "wyczyść");

            grammarBuilder = new GrammarBuilder();
            grammarBuilder.Append(words);

            enumerator = new MMDeviceEnumerator();
            grammar = new Grammar(grammarBuilder);
            dataTable = new DataTable();
            dataTable.Columns.Add("expression", typeof(string));
            recognizer.LoadGrammar(grammar);
            labelEquation.Content = "";
            recognizer.SpeechRecognized += (s, e) =>
            {
                labelAudioRecordingStatus.Content = "Rejestrowanie: Aktywne";
                if (e.Result != null && e.Result.Confidence > 0.5)
                {
                    string recognizedText = e.Result.Text;
                    update(recognizedText);
                }
            };
            labelAudioRecordingStatus.Content = "Rejestrowanie: Aktywne";
            recognizer.SetInputToDefaultAudioDevice();
            recognizer.RecognizeAsync(RecognizeMode.Multiple);

            var defaultDevice = enumerator.GetDefaultAudioEndpoint(DataFlow.Capture, Role.Console);
            labelAudioInputDevice.Content += defaultDevice.FriendlyName;

            speechSynthesizer = new SpeechSynthesizer();
            speechSynthesizer.SetOutputToDefaultAudioDevice();
        }

        private void showHelp(object sender, RoutedEventArgs e)
        {
            HelpWindow helpWindow = new HelpWindow();
            helpWindow.ShowDialog();
        }

        private void showAbout(object sender, RoutedEventArgs e)
        {
            AboutWindow aboutDialogWindow = new AboutWindow();
            aboutDialogWindow.ShowDialog();
        }

        private void update(string text)
        {
            if (Regex.IsMatch(text, "^[0-9]$"))
            {
                labelEquation.Content += text;
            }
            else
            {
                switch (text)
                {
                    case "dodaj":
                    case "dodać":
                    case "plus":
                        labelEquation.Content += " + ";
                        break;

                    case "odejmij":
                    case "odjąć":
                    case "minus":
                        labelEquation.Content += " - ";
                        break;

                    case "pomnóż":
                    case "razy":
                    case "mnożyć":
                        labelEquation.Content += " * ";
                        break;

                    case "podziel":
                    case "podzielić":
                    case "dziel":
                    case "przez":
                        labelEquation.Content += " / ";
                        break;

                    case "wyczyść":
                        labelEquation.Content = "";
                        break;

                    case "wykonaj":
                        string equation = labelEquation.Content.ToString();
                        string[] parts = equation.Split(' ');

                        if (parts.Length != 3)
                        {
                            labelEquation.Content = "Niepoprawne";
                            speechSynthesizer.SpeakAsync(labelEquation.Content.ToString());
                            break;
                        }

                        int leftOperand, rightOperand;

                        if (!int.TryParse(parts[0], out leftOperand) || !int.TryParse(parts[2], out rightOperand))
                        {
                            labelEquation.Content = "Niepoprawne";
                            speechSynthesizer.SpeakAsync(labelEquation.Content.ToString());
                            break;
                        }

                        string resultAsString = "", leftOperandAsString = "", operatorAsString = "", rightOperandAsString = "";

                        int result = 0;
                        switch (parts[1])
                        {
                            case "+":
                                result = leftOperand + rightOperand;
                                resultAsString = result.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                leftOperandAsString = leftOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                operatorAsString = "dodać";
                                rightOperandAsString = rightOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                break;
                            case "-":
                                result = leftOperand - rightOperand;
                                resultAsString = result.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                leftOperandAsString = leftOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                operatorAsString = "odjąć";
                                rightOperandAsString = rightOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                break;
                            case "*":
                                result = leftOperand * rightOperand;
                                resultAsString = result.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                leftOperandAsString = leftOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                operatorAsString = "razy";
                                rightOperandAsString = rightOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                break;
                            case "/":
                                if (rightOperand == 0)
                                {
                                    labelEquation.Content = "Nie dzielimy przez 0";
                                    return;
                                }
                                result = leftOperand / rightOperand;
                                resultAsString = result.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                leftOperandAsString = leftOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                operatorAsString = "podzielić przez";
                                rightOperandAsString = rightOperand.ToWords(new System.Globalization.CultureInfo("pl-PL"));
                                break;
                        }
                        string resultToPrint = labelEquation.Content + " = " + result.ToString();
                        labelEquation.Content = resultToPrint;
                        string resultToSpeech = "Wynik to " + resultAsString;
                        speechSynthesizer.SpeakAsync(resultToSpeech);
                        break;
                }
            }
        }
    }
}
