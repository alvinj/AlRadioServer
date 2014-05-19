import play.api._

import scala.collection.JavaConversions._

object Global extends GlobalSettings {
  
  var plsFileLocation: Option[String] = None
  var radioStations: Option[List[Double]] = None
  var onlineStreams: Option[List[(String, String)]] = None

  override def onStart(app: Application) {
      // populate these values from the application.conf file
      populatePlsFileLocation
      populateRadioStations
      populateListOfStreams
  }
  
  // something like "/var/tmp/plsfiles"
  private def populatePlsFileLocation {
      val loc = Some(play.Play.application.configuration.getString("plsFileLocation"))
      if (loc != null) plsFileLocation = loc
  }
  
  private def populateRadioStations {
      val stationsList = play.Play.application.configuration.getDoubleList("stations")
      if (stationsList != null) {
          val stations = stationsList.map { station => 
              station.toDouble
          }.toList
          radioStations = Some(stations)
      }
  }
  
  private def populateListOfStreams {
      val streamsList = play.Play.application.configuration.getConfigList("streams")
      if (streamsList != null) {
          val streams = streamsList.map { cfg => 
              val name = cfg.getString("streamname")
              val filename = cfg.getString("filename")
              name -> filename
          }.toList
          onlineStreams = Some(streams)
      }
  }

  override def onStop(app: Application) {
      Logger.info("Application shutdown...")
  }  
    
}










