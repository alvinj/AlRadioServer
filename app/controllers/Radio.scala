package controllers

import play.api._
import play.api.mvc._
import utils._
import play.api.libs.json._
import play.api.libs.json.Json
import play.api.libs.json.Json._
import models.RadioStation
import models.RadioStream
import java.io.File

/**
 * A "PLS" file is a file that contains one or more URLs for radio streams.
 * See the wgn.pls or 104_3.pls files in this project for examples of what they contains.
 * The important thing is that if you give VLC one of those files, it knows how to handle it to open an
 * online stream to that radio station/service.
 */
object Radio extends Controller {
  
    // TODO get these as options (or, leave as is, and let the app crash)
    val vlcHost = play.Play.application.configuration.getString("vlc_host")
    val vlcPort = play.Play.application.configuration.getInt("vlc_port")
    val radioServerHost = play.Play.application.configuration.getString("radio_server_host")
    val radioServerPort = play.Play.application.configuration.getInt("radio_server_port")

    def index = Action {
        Ok(views.html.index("Welcome to AlRadio!"))
    }

    /**
     * output:
     * 
     * [
     *     {"number" : "88.5", "description": "public radio"},
     *     {"number" : "102.3", "description": "espn"},
     *     {"number" : "104.3", "description": "denver sports"}
     * ]
     * 
     */
    def getRadioStations = Action {
        val stationsOption = loadListOfRadioStationsAsObjects
        stationsOption match {
            case Some(stations) =>
                // implicit val radioStationFormat = Json.format[RadioStation]
                Ok(Json.toJson(stations))
            case None =>
                Ok(Json.toJson(Map("success" -> toJson(false), "msg" -> toJson("Could not load the list of radio stations."))))
        }
    }
    
    /**
     * output:
     * 
     * [
     *     {"name" : "104.3"},
     *     {"name" : "WGN"}
     * ]
     * 
     */
    def getRadioStreams = Action {
        val streamsOption = loadListOfRadioStreamsForClients
        streamsOption match {
            case Some(streams) =>
                Ok(Json.toJson(streams))
            case None =>
                Ok(Json.toJson(Map("success" -> toJson(false), "msg" -> toJson("Could not load the list of radio streams."))))
        }
    }

    /**
     * Get the recordings we have (stream recordings).
     */
    def getRecordings = Action {
        val recordingsDir = getRecordingsDir
        val recordings = getListOfRecordings(recordingsDir)
        // TODO i'm short on time, and just assuming success here
        Ok(Json.toJson(recordings))
    }
    
    /**
     * val okFileExtensions = List("wav", "mp3")
     * val files = getListOfFiles(new File("/tmp"), okFileExtensions)
     */
    private def getListOfRecordings(recordingsDir: String): List[String] = {
        val d = new File(recordingsDir)
        if (d.exists && d.isDirectory) {
            d.listFiles.filter(_.isFile).map(_.getName).toList
        }
        else {
            List[String]() 
        }
    }
    
    private def getRecordingsDir = play.Play.application.configuration.getString("recordings_dir")
    
    
    /**
     * FM Radio Services
     * -----------------
     */

    // TODO i'm just assuming success here
    def tuneRadio(station: String) = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        try {
            NetworkUtils.writeCommandToSocket(radioServerHost, radioServerPort, s"GET /tune/${station}\n\n")
        } catch {
            case t: Throwable => t.printStackTrace 
        }
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    // TODO i'm just assuming success here
    def turnRadioOff = Action {
        // shutdownVlcIfItsRunning(vlcHost, vlcPort)
        handleTurnRadioOffCommand
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }

    def turnEverythingOff = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        handleTurnRadioOffCommand
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }

    private def handleTurnRadioOffCommand {
        try {
            NetworkUtils.writeCommandToSocket(radioServerHost, radioServerPort, s"GET /turn_off\n\n")
        } catch {
            case t: Throwable => t.printStackTrace 
        }
    }

    /**
     * change the volume using the linux `alsa` utilities.
     */
    def setVolume(volume: Int) = Action {
        try {
            AlsaUtils.setVolume(volume)
        } catch {
            case t: Throwable => t.printStackTrace 
        }
        // TODO i just assume success here
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    

    /**
     * VLC-Based Services
     * ------------------
     */
    
    def playRecording(recordingFilename: String) = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        stopRadioIfItsRunning
        val canonFilename = getRecordingsDir + "/" + recordingFilename
        startVlcStreamServer(vlcHost, vlcPort, canonFilename)
        // TODO again, i'm short on time, and just assuming success here
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    /**
     * Given an online stream name like "WGN", play its stream.
     */
    def playStream(streamName: String) = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        stopRadioIfItsRunning
        val canonFilenameOption = getPlsCanonFilenameFromStreamName(streamName)
        val result = startVlcServerWithPlsFile(canonFilenameOption)
        result
    }
    
    private def startVlcServerWithPlsFile(canonFilenameOption: Option[String]) = {
        canonFilenameOption match {
            case Some(canonFilename) =>
                startVlcStreamServer(vlcHost, vlcPort, canonFilename)
                Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
            case None => 
                NotAcceptable(Json.toJson(Map("success" -> toJson(false), "msg" -> toJson("Something went 'Boom!'"))))
        }
    }
    
    // TODO check to see if the radio is running before trying to shut it down
    private def stopRadioIfItsRunning { 
        handleTurnRadioOffCommand
    }
    
    private def shutdownVlcIfItsRunning(host: String, port: Int) {
        // TODO check to see if it's running first
        try {
            VlcUtils.shutdown(host, port)
        } catch {
            case e: Exception => //
        }
    }
    
    def pauseVlc = Action {
        VlcUtils.pause(vlcHost, vlcPort)
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    def playVlc = Action {
        VlcUtils.play(vlcHost, vlcPort)
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    // turnVlcOff
    def shutdownVlc = Action {
        VlcUtils.shutdown(vlcHost, vlcPort)
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    private def getPlsCanonFilenameFromStreamName(streamName: String): Option[String] = {
        val dirOption = getPlsFileLocation
        val streamsOption = getListOfStreams
        val filenameOption = streamsOption.map(_(streamName))
        for {
            dir <- dirOption
            filename <- filenameOption
        } yield s"$dir/$filename"
    }

    private def getListOfStreams: Option[Map[String, String]] = {
        import scala.collection.JavaConversions._
        val streamsList = play.Play.application.configuration.getConfigList("streams")
        if (streamsList != null) {
            val streams = streamsList.map { cfg => 
                val name = cfg.getString("streamname")
                val filename = cfg.getString("filename")
                name -> filename
            }.toMap
            Some(streams)
        } else {
            None
        }
    }
    
    /**
     * TODO if i decide that it's better for `number` to be a BigDecimal, this code
     * may work (untested).
     */
    private def loadListOfRadioStationsAsObjects: Option[List[RadioStation]] = {
        import scala.collection.JavaConversions._
        val stationsList = play.Play.application.configuration.getConfigList("stations")
        if (stationsList != null) {
            val stations = stationsList.map { cfg =>
                RadioStation(BigDecimal(cfg.getDouble("number")), cfg.getString("description"))
            }.toList
            Some(stations)
        } else {
            None
        }
    }

    /**
     * I'm treating the "number" as a String. It may be better to treat it as a
     * BigDecimal, but that is more work.
     */
    private def loadListOfRadioStations: Option[Map[String, String]] = {
        import scala.collection.JavaConversions._
        val stationsList = play.Play.application.configuration.getConfigList("stations")
        if (stationsList != null) {
            val stations = stationsList.map { cfg => 
                val number = cfg.getString("number")
                val description = cfg.getString("description")
                number -> description
            }.toMap
            Some(stations)
        } else {
            None
        }
    }

    // stream = (streamname, filename)
    private def loadListOfRadioStreamsForClients: Option[List[RadioStream]] = {
        import scala.collection.JavaConversions._
        val streamsList = play.Play.application.configuration.getConfigList("streams")
        if (streamsList != null) {
            val streams = streamsList.map { cfg =>
                // `filename` is ignored by the json `writes` method
                RadioStream(cfg.getString("streamname"), cfg.getString("filename"))
            }.toList
            Some(streams)
        } else {
            None
        }
    }

    private def getPlsFileLocation: Option[String] = {
        val loc = play.Play.application.configuration.getString("plsFileLocation")
        if (loc != null) Some(loc) else None
    }

    /**
     * Start a stream, like "wgn.pls" or "104_3.pls".
     */
    private def startVlcStreamServer(host: String, port: Int, canonPlsFile: String) {
        val cmd = VlcUtils.buildVlcStreamServerCommand(host, port, canonPlsFile)
        VlcUtils.executeCommand(cmd)
    }
    
    

}













