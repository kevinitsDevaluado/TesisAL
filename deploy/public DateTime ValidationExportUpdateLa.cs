public DateTime ValidationExportUpdateLast()
        {
            td_parameters_services _parameter = new td_parameters_services();
            DateTime update;
            try
            {
                using (var db = OpenDbShopWas())
                {
                    _parameter = db.td_parameters_servicis.Where(l => l.Key.Equals("ExportBOLastExecution")).FirstOrDefault();
                }
                
                update = _parameter != null ? _parameter.LastUpdate : DateTime.Now;
            }
            catch (Exception ex)
            {
                update = DateTime.Now;
            }
            return update;
        }