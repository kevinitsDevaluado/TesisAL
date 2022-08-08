using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using GLS.Shop.Core.Classes;
using GLS.Shop.DAL;
using GLS.Shop.DAL.DB.ProntoPacco.Was;
using GLS.Shop.DAL.DB.ProntoPacco;
using GLS.Shop.Core.Models;
using Newtonsoft.Json;
using Microsoft.EntityFrameworkCore;

namespace GLS.Shop.Core
{
    public class BusinessObjetsManager
    {
        private string connectionString = string.Empty;


        public BusinessObjetsManager(string mySqlConnectionString)
        {
            this.connectionString = mySqlConnectionString;
        }
        private DB OpenDbShopWas()
        {
            return new DB(DAL.Extensions.CreateMySqlOptions<DAL.DB.ProntoPacco.Was.DB>(connectionString));
        }

        

        public async void Update_Td_Parameters_Services(DateTime _lastDate)
        {
            DateTime currentDay = _lastDate;
            using ( var db = OpenDbShopWas())
            {
                td_parameters_services _parameter = new td_parameters_services();
                
                _parameter = db.td_parameters_servicis.Where(l => l.Key.Equals("ExportBOLastExecution")).FirstOrDefault();

                _parameter.LastUpdate = currentDay;
                db.Update(_parameter);
                await db.SaveChangesAsync();
            }
        }

        public string Export_Spedizione_Was_Json( int limit)
        {
            DateTime startDate;
            DateTime endDate;
            DateTime update;
            string jsonData = "";
            string jsonResult = "";
            DateTime lastDay = DateTime.Now.AddDays(-1);
            startDate = new DateTime(lastDay.Year, lastDay.Month, 1, 0, 0, 0);
            endDate = new DateTime(lastDay.Year, lastDay.Month, 30, 23, 59, 59);
            List<tab_spedizione_wasDTOExportJson> list = new List<tab_spedizione_wasDTOExportJson>();
            List<tab_spedizione_wasDTOExportJson> finalList = new List<tab_spedizione_wasDTOExportJson>();
            td_parameters_services _parameter = new td_parameters_services();
            try
            {
                using (var db = OpenDbShopWas())
                {
                    int _page = 1;
                    list = new List<tab_spedizione_wasDTOExportJson>();
                    
                    do
                    {
                        int _limit = limit;
                        int _offset = (_page * _limit) - _limit;
                        _parameter = db.td_parameters_servicis.Where(l => l.Key.Equals("ExportBOLastExecution")).FirstOrDefault();
                        update = _parameter != null ? _parameter.LastUpdate : DateTime.Now;
                        list = db.tab_spedizioni_was.Where(x => ((x.data_inserimento > update) ||
                                                      (x.data_ultima_modifica > update))
                                        ).Select(s => new tab_spedizione_wasDTOExportJson()
                                        {
                                            id_sped = s.id_sped,
                                            partner_ids = s.partner_id,
                                            parcelShopId = s.parcelShopId,
                                            shipmentID = s.shipmentID,
                                            sede_pi = s.sede_pi,
                                            sede_rif_pi = s.sede_rif_pi,
                                            zona_pi = s.zona_pi,
                                            barcode = s.barcode,
                                            destinatario = s.destinatario,
                                            email = s.email,
                                            telefono = s.telefono,
                                            ddt = Convertion.Null2String(s.ddt),
                                            bda = Convertion.Null2String(s.bda),
                                            num_colli = s.num_colli,
                                            peso = s.peso,
                                            peso_volume = s.peso_volume,
                                            tipo_sped = s.tipo_sped,
                                            svincolo_mittente = Convertion.Null2String(s.svincolo_mittente),
                                            nominativo_ritirante = Convertion.Null2String(s.nominativo_ritirante),
                                            firma = s.firma,
                                            stato_corrente = s.stato_corrente,
                                            data_inserimento = s.data_inserimento,
                                            data_ultima_modifica = s.data_ultima_modifica,
                                            utente_ultima_modifica = s.utente_ultima_modifica
                                        }).Skip(_offset).Take(_limit).ToList();
                        finalList.AddRange(list);
                        _page++;
                    } while (list.Count() > 0);

                }
                jsonData = JsonConvert.SerializeObject(finalList);
                jsonResult = "{\"spedizioni\":" + jsonData + @"}";
            }
            catch (Exception ex)
            {
                jsonResult = String.Empty;
            }
            return jsonResult;
        }

        public string Export_Spedizione_Stati_Was_Json(int limit)
        {
            DateTime startDate;
            DateTime endDate;
            string jsonData = "";
            string jsonResult = "";
            DateTime lastDay = DateTime.Now.AddDays(-1);
            startDate = new DateTime(lastDay.Year, lastDay.Month, 1, 0, 0, 0);
            endDate = new DateTime(lastDay.Year, lastDay.Month, 30, 23, 59, 59);
            
            DateTime update;
            td_parameters_services _parameter = new td_parameters_services();
            List<tab_spedizione_stato_wasDTOExportJson> list = new List<tab_spedizione_stato_wasDTOExportJson>();
            List<tab_spedizione_stato_wasDTOExportJson> finalList = new List<tab_spedizione_stato_wasDTOExportJson>();

            try
            {
                using (var db = OpenDbShopWas())
                {
                    int _page = 1;
                    list = new List<tab_spedizione_stato_wasDTOExportJson>();
                    do
                    {
                        int _limit = limit;
                        int _offset = (_page * _limit) - _limit;
                        _parameter = db.td_parameters_servicis.Where(l => l.Key.Equals("ExportBOLastExecution")).FirstOrDefault();
                        update = _parameter != null ? _parameter.LastUpdate : DateTime.Now;
                        list = db.tab_spedizioni_stati_was.Where(x => x.data_inserimento_stato > update
                                                      ).Select(s => new tab_spedizione_stato_wasDTOExportJson()
                                                      {
                                                          id_stato = s.id_stato,
                                                          id_sped = s.id_sped,
                                                          stato = s.stato,
                                                          causale_richiesta_ritiro = s.causale_richiesta_ritiro,
                                                          dataora_evento_da_3P = s.dataora_evento_da_3P == null ? "" : ((DateTime)s.dataora_evento_da_3P).ToString(),
                                                          partner_ids = s.partner_id,
                                                          parcelShopId = s.parcelShopId,
                                                          shipmentID = s.shipmentID,
                                                          sede_pi = s.sede_pi,
                                                          sede_rif_pi = s.sede_rif_pi,
                                                          zona_pi = s.zona_pi,
                                                          barcode = s.barcode,
                                                          destinatario = s.destinatario,
                                                          email = s.email,
                                                          telefono = s.telefono,
                                                          ddt = Convertion.Null2String(s.ddt),
                                                          bda = Convertion.Null2String(s.bda),
                                                          num_colli = (decimal)s.num_colli,
                                                          peso = (decimal)s.peso,
                                                          peso_volume = (decimal)s.peso_volume,
                                                          tipo_sped = s.tipo_sped,
                                                          svincolo_mittente = Convertion.Null2String(s.svincolo_mittente),
                                                          nominativo_ritirante = Convertion.Null2String(s.nominativo_ritirante),
                                                          firma = (bool)s.firma,
                                                          stato_aggiornato_da_utente = s.stato_aggiornato_da_utente ? "1" : "0",
                                                          stato_aggiornato_da_servizio = s.stato_aggiornato_da_servizio ? "1" : "0",
                                                          data_inserimento_stato = s.data_inserimento_stato.ToString(),
                                                          utente_ultima_modifica = s.utente_ultima_modifica
                                                      }).Skip(_offset).Take(_limit).ToList();
                        finalList.AddRange(list);
                        _page++;
                    } while (list.Count() > 0);
                    jsonData = JsonConvert.SerializeObject(finalList);
                    jsonResult = "{\"stati\":" + jsonData + @"}";
                }
            }
            catch (Exception ex)
            {
                jsonResult = String.Empty;
            }
            return jsonResult;
        }

        public string Export_Shop_Was_Json(int limit)
        {
            DateTime startDate;
            DateTime endDate;
            string jsonData = "";
            string jsonResult = "";
            DateTime lastDay = DateTime.Now.AddDays(-1);
            startDate = new DateTime(lastDay.Year, lastDay.Month, 1, 0, 0, 0);
            endDate = new DateTime(lastDay.Year, lastDay.Month, 30, 23, 59, 59);
            List<tab_shop_wasDTOExportJson> list = new List<tab_shop_wasDTOExportJson>();
            List<tab_shop_wasDTOExportJson> finalList = new List<tab_shop_wasDTOExportJson>();
            try
            {
                using (var db = OpenDbShopWas())
                {
                    int _page = 1;
                    list = new List<tab_shop_wasDTOExportJson>();
                    do
                    {
                        int _limit = limit;
                        int _offset = (_page * _limit) - _limit;
                        list = db.tab_shop_was.Include("attributes").Where(x =>
                                                                (
                                                                  (x.Data_inserimento >= startDate &&
                                                                   x.Data_inserimento <= endDate) ||
                                                                  (x.Data_ultima_modifica >= startDate &&
                                                                   x.Data_ultima_modifica <= endDate)
                                                                )
                                                               ).
                                                       Select(s => new tab_shop_wasDTOExportJson()
                                                       {
                                                           partner_ids = s.partner_id,
                                                           parcelShopId = s.parcelShopId,
                                                           name = s.name,
                                                           additionalInfo = s.additionalInfo,
                                                           email = s.email,
                                                           phone = s.phone,
                                                           countryCode = s.countryCode,
                                                           province = s.province,
                                                           city = s.city,
                                                           street = s.street,
                                                           houseNumber = s.houseNumber,
                                                           latitude = s.latitude,
                                                           longitude = s.longitude,
                                                           activeFrom = s.activeFrom,
                                                           activeTo = s.activeTo,
                                                           saturation_level = s.saturation_level,
                                                           product_category = (int)s.product_category,
                                                           shop_area = s.shop_area,
                                                           employees_number = s.employees_number,
                                                           in_net_since = s.in_net_since,
                                                           dedicated_storage_area = Convertion.Bool2Short(s.dedicated_storage_area),
                                                           tvcc = Convertion.Bool2Short(s.tvcc),
                                                           intrusion_alarms = Convertion.Bool2Short(s.intrusion_alarms),
                                                           surveillance = Convertion.Bool2Short(s.surveillance),
                                                           strong_joinery = Convertion.Bool2Short(s.strong_joinery),
                                                           sede = s.sede,
                                                           zona = s.zona,
                                                           shop_disabilitato_automaticamente = Convertion.Bool2Short(s.shop_disabilitato_automaticamente),
                                                           shop_disabilitato_manualmente = Convertion.Bool2Short(s.shop_disabilitato_manualmente),
                                                           Data_inserimento = s.Data_inserimento.ToString(),
                                                           Data_ultima_modifica = s.Data_ultima_modifica.ToString(),
                                                           Stato = (int)s.Stato,
                                                           ID_anagrafica_contabile = s.attributes.accountingRegistryID == null ? string.Empty : s.attributes.accountingRegistryID,
                                                           shop_monomarca = 0, // We have to find this field
                                                           chiusura_definitiva = Convertion.Bool2Short(s.attributes.finalClosing),
                                                           chiusura_definitiva_da_utente = s.attributes.finalClosingUser == null ? string.Empty : s.attributes.finalClosingUser,
                                                           data_chiusura_definitiva = s.attributes.finalClosingDate == null ? string.Empty : s.attributes.finalClosingDate.ToString(),
                                                           approvazione_sales = Convertion.Bool2Short(s.attributes.salesApproval),
                                                           approvazione_sales_timestamp = s.attributes.salesApprovalDate == null ? string.Empty : s.attributes.salesApprovalDate.ToString(),
                                                           approvazione_sales_utente = s.attributes.salesApprovalUser,
                                                           approvazione_rae = Convertion.Bool2Short(s.attributes.raeApproval),
                                                           approvazione_rae_timestamp = s.attributes.raeApprovalDate == null ? string.Empty : s.attributes.raeApprovalDate.ToString(),
                                                           approvazione_rae_utente = s.attributes.raeApprovalUser == null ? string.Empty : s.attributes.raeApprovalUser
                                                       }).Skip(_offset).Take(_limit).ToList();
                        finalList.AddRange(list);
                        _page++;
                    } while (list.Count() > 0);
                    jsonData = JsonConvert.SerializeObject(finalList);
                    jsonResult = "{\"shops\":" + jsonData + @"}";
                }
            }
            catch (Exception ex)
            {
                jsonResult = String.Empty;
            }
            return jsonResult;
        }

        public string Export_Shop_Working_Days_Was_Json(int limit)
        {
            DateTime startDate;
            DateTime endDate;
            string jsonData = "";
            string jsonResult = "";
            DateTime lastDay = DateTime.Now.AddDays(-1);
            startDate = new DateTime(lastDay.Year, lastDay.Month, lastDay.Day, 0, 0, 0);
            endDate = new DateTime(lastDay.Year, lastDay.Month, lastDay.Day, 23, 59, 59);
            List<tab_shop_working_days_wasDTOExportJson> list = new List<tab_shop_working_days_wasDTOExportJson>();
            List<tab_shop_working_days_wasDTOExportJson> finalList = new List<tab_shop_working_days_wasDTOExportJson>();
            try
            {
                using (var db = OpenDbShopWas())
                {
                    int _page = 1;
                    list = new List<tab_shop_working_days_wasDTOExportJson>();
                    do
                    {
                        int _limit = limit;
                        int _offset = (_page * _limit) - _limit;
                        list = db.tab_shop_working_days_was.Where(x => (x.Data_ultima_modifica >= startDate &&
                                                            x.Data_ultima_modifica <= endDate)).
                                                Select(s => new tab_shop_working_days_wasDTOExportJson()
                                                {
                                                    partner_ids = s.partner_id,
                                                    parcelShopId = s.parcelShopId,
                                                    weekday = Convertion.Weekday2Short(s.weekday),
                                                    openingTime = s.openingTime.ToString(),
                                                    closingTime = s.closingTime.ToString(),
                                                    validFrom = s.validFrom.ToString(),
                                                    Data_ultima_modifica = s.Data_ultima_modifica.ToString()
                                                }).Skip(_offset).Take(_limit).ToList();
                        finalList.AddRange(list);
                        _page++;
                    } while (list.Count() > 0 /*&& _page < 3*/);
                    jsonData = JsonConvert.SerializeObject(finalList);
                    jsonResult = "{\"workingdays\":" + jsonData + @"}";
                }
            }
            catch (Exception ex)
            {
                jsonResult = String.Empty;
            }
            return jsonResult;
        }

        public string Export_Shop_Vacation_Was_Json(int limit)
        {
            DateTime startDate;
            DateTime endDate;
            string jsonData = "";
            string jsonResult = "";
            DateTime lastDay = DateTime.Now.AddDays(-1);
            startDate = new DateTime(1, 1, 1, 0, 0, 0);
            endDate = new DateTime(1, lastDay.Month, 30, 23, 59, 59);
            List<tab_shop_vacation_wasDTOExportJson> list;
            List<tab_shop_vacation_wasDTOExportJson> finalList = new List<tab_shop_vacation_wasDTOExportJson>();
            try
            {
                using (var db = OpenDbShopWas())
                {
                    int _page = 1;
                    list = new List<tab_shop_vacation_wasDTOExportJson>();
                    do
                    {
                        int _limit = limit;
                        int _offset = (_page * _limit) - _limit;
                        list = db.tab_shop_vacation_was.Where(x => (x.Data_ultima_modifica >= startDate &&
                                                                    x.Data_ultima_modifica <= endDate)).
                                                        Select(s => new tab_shop_vacation_wasDTOExportJson()
                                                        {
                                                            partner_ids = s.partner_id,
                                                            parcelShopId = s.parcelShopId,
                                                            startDate = s.startDate.ToString(),
                                                            endDate = s.endDate.ToString(),
                                                            Data_ultima_modifica = s.Data_ultima_modifica.ToString()
                                                        }).Skip(_offset).Take(limit).ToList();
                        finalList.AddRange(list);
                        _page++;
                    } while (list.Count() > 0);
                }
                jsonData = JsonConvert.SerializeObject(finalList);
                jsonResult = "{\"vacations\":" + jsonData + @"}";
            }
            catch (Exception ex)
            {
                jsonResult = String.Empty;
            }
            return jsonResult;
        }

        public string Export_V_Lastshoperror_Json(int limit)
        {

            string jsonData = "";
            string jsonResult = "";
            List<v_lastshoperrorDTOExportJson> list;
            List<v_lastshoperrorDTOExportJson> finalList = new List<v_lastshoperrorDTOExportJson>();
            try
            {
                using (var db = OpenDbShopWas())
                {
                    int _page = 1;
                    list = new List<v_lastshoperrorDTOExportJson>();
                    do
                    {
                        int _limit = limit;
                        int _offset = (_page * _limit) - _limit;
                        list = db.v_lastshopirror.Select(s => new v_lastshoperrorDTOExportJson()
                                                        {
                                                            partnerShopID = s.partnerShopID,
                                                            parcelShopID = s.parcelShopID,
                                                            DATETIME = s.DATETIME.ToString(),
                                                            LogMessage = s.Message,
                                                            Source = s.SOURCE
                                                        }).Skip(_offset).Take(limit).ToList();
                        finalList.AddRange(list);
                        _page++;
                    } while (list.Count() > 0);
                }
                jsonData = JsonConvert.SerializeObject(finalList);
                jsonResult = "{\"shops\":" + jsonData + @"}";
            }
            catch (Exception ex)
            {
                jsonResult = String.Empty;
            }
            return jsonResult;
        }

    }

}
><