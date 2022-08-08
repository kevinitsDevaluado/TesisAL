using GLS.Shop.DAL;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;

namespace GLS.Shop.ShopBusinessObjectsWorkerService
{
    public class Program
    {
        public static int Main(string[] args)
        {
            AppDomain.CurrentDomain.UnhandledException += CurrentDomain_UnhandledException;
            ConsoleProgram.IncludeTimeStamp = true;
            int returnCode = 0;
            // command line parser see (https://docs.microsoft.com/en-us/dotnet/api/microsoft.extensions.configuration.commandlineconfigurationextensions.addcommandline?view=dotnet-plat-ext-6.0)
            var builder = new ConfigurationBuilder().AddCommandLine(args);
            var config = builder.Build();
            try
            {
                string strExport = config["export"];
                bool export = false;
                if (!strExport.IsNullOrEmptyOrWhiteSpace() && bool.TryParse(strExport, out export) && export)
                {
                    ConsoleProgram.Info("Starting Business Objects.");
                    CreateHostBuilder(args).Build();
                    Startup.Log.Info($"BO. cliParams; --export={strExport}. config file params Startup.OutBasePath={Startup.OutBasePath}");
                    Startup.Log.Info("Avvio Controllo");

                    string Path = Startup.OutBasePath;


                    bool result = ExportData(export, Path);

                    ConsoleProgram.Success("BO. Console Application. ended. Output in Startup.Log4net.");
                }
                else
                {
                    CreateHostBuilder(args).Build().Run();
                }

                returnCode = 0;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex);
                returnCode = 1;
            }

            return returnCode;
        }
        
        public static bool ExportData(bool _export, string _path)
        {
            bool result = false;
            Startup.Log.Info("Start BusinessObjectsWorkerService exportation");
            //Startup.Logger.Info("Start ModuleAS400WorkerService.");

            Shop.Core.Controllers.ExportBOController exportBO = new Shop.Core.Controllers.ExportBOController();
            try
            {
                var _lastUpdateDate = exportBO.UpdateLast();
                DateTime currentDay = DateTime.Now;
                if (currentDay > _lastUpdateDate)
                {

                }
                string currentPath = Path.Combine(_path, $"spedizioni_was.json");

                int _limit = 40;
                var _shippingData = exportBO.ExportSpedizione(_export, _limit);
                bool _directoryExists = File.Exists(currentPath);
                Startup.Log.Info("Export Business Objects (tab_spedizioni_was) Path: " + currentPath);

                if (_directoryExists)
                {
                    File.Delete(currentPath);
                }

                if (_shippingData != null && _shippingData.Length > 0)
                {

                    StreamWriter st = new StreamWriter(currentPath, true);
                    st.WriteLine(_shippingData);
                    st.Close();

                }
                currentPath = Path.Combine(_path, $"spedizioni_stati_was.json");

                _limit = 40;
                _shippingData = exportBO.ExportSpedizioneStato(_export, _limit);
                _directoryExists = File.Exists(currentPath);
                Startup.Log.Info("Export Business Objects (tab_spedizioni_stati_was) Path: " + currentPath);

                if (_directoryExists)
                {
                    File.Delete(currentPath);
                }

                if (_shippingData != null && _shippingData.Length > 0)
                {

                    StreamWriter st = new StreamWriter(currentPath, true);
                    st.WriteLine(_shippingData);
                    st.Close();

                }

                currentPath = Path.Combine(_path, $"shop.json");

                _limit = 40;
                _shippingData = exportBO.ExportShopWas(_export, _limit);
                _directoryExists = File.Exists(currentPath);
                Startup.Log.Info("Export Business Objects (tab_shop_was) Path: " + currentPath);

                if (_directoryExists)
                {
                    File.Delete(currentPath);
                }

                if (_shippingData != null && _shippingData.Length > 0)
                {

                    StreamWriter st = new StreamWriter(currentPath, true);
                    st.WriteLine(_shippingData);
                    st.Close();

                }


                currentPath = Path.Combine(_path, $"shop_workingdays.json");

                _limit = 40;
                _shippingData = exportBO.ExportShopWorkinDaysWas(_export, _limit);
                _directoryExists = File.Exists(currentPath);
                Startup.Log.Info("Export Business Objects (tab_shop_working_days_was) Path: " + currentPath);

                if (_directoryExists)
                {
                    File.Delete(currentPath);
                }

                if (_shippingData != null && _shippingData.Length > 0)
                {

                    StreamWriter st = new StreamWriter(currentPath, true);
                    st.WriteLine(_shippingData);
                    st.Close();

                }

                currentPath = Path.Combine(_path, $"shop_vacation.json");

                _limit = 40;
                _shippingData = exportBO.ExportShopVacationWas(_export, _limit);
                _directoryExists = File.Exists(currentPath);
                Startup.Log.Info("Export Business Objects (tab_shop_vacation_was) Path: " + currentPath);

                if (_directoryExists)
                {
                    File.Delete(currentPath);
                }

                if (_shippingData != null && _shippingData.Length > 0)
                {

                    StreamWriter st = new StreamWriter(currentPath, true);
                    st.WriteLine(_shippingData);
                    st.Close();

                }

                currentPath = Path.Combine(_path, $"ShopImportLog.json");

                _limit = 40;
                _shippingData = exportBO.ExportVLastShopError(_export, _limit);
                _directoryExists = File.Exists(currentPath);
                Startup.Log.Info("Export Business Objects (v_lastshoperror) Path: " + currentPath);

                if (_directoryExists)
                {
                    File.Delete(currentPath);
                }

                if (_shippingData != null && _shippingData.Length > 0)
                {

                    StreamWriter st = new StreamWriter(currentPath, true);
                    st.WriteLine(_shippingData);
                    st.Close();

                }

            }
            catch (Exception ex)
            {
                Startup.Log.Error(ex.Message);
            }

            return result;
        }

        private static void CurrentDomain_UnhandledException(object sender, UnhandledExceptionEventArgs e)
        {
            try
            {
                var exception = (Exception)e.ExceptionObject;
                ConsoleProgram.Error($"IsTerminating: {e.IsTerminating}\r\nMessage: {exception.Message}\r\nStack: {exception.StackTrace}");
            }
            catch (Exception ex)
            {
                ConsoleProgram.Error($"Message: {ex.Message}\r\nStack: {ex.StackTrace}");
            }
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
