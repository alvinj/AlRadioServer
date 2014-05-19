import play.api._

import scala.collection.JavaConversions._

object Global extends GlobalSettings {
  
//  var plsFileLocation: Option[String] = None
//  var radioStations: Option[List[Double]] = None
//  var onlineStreams: Option[List[(String, String)]] = None

  override def onStart(app: Application) {
  }
  
//  private def populateRadioStations {
//      val stationsList = play.Play.application.configuration.getDoubleList("stations")
//      if (stationsList != null) {
//          val stations = stationsList.map { station => 
//              station.toDouble
//          }.toList
//          radioStations = Some(stations)
//      }
//  }
  
  override def onStop(app: Application) {
      Logger.info("Application shutdown...")
  }  
    
}

