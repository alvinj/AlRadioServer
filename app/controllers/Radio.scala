package controllers

import play.api._
import play.api.mvc._
import utils._
import play.api.libs.json._
import play.api.libs.json.Json
import play.api.libs.json.Json._

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

    // TODO i'm just assuming success here
    def tuneRadio(station: String) = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        NetworkUtils.writeCommandToSocket(radioServerHost, radioServerPort, s"GET /tune/${station}\n\n")
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    // TODO i'm just assuming success here
    def turnRadioOff = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        NetworkUtils.writeCommandToSocket(radioServerHost, radioServerPort, s"GET /turn_off\n\n")
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    /**
     * Given an online stream name like "WGN", play its stream.
     */
    def playStream(streamName: String) = Action {
        shutdownVlcIfItsRunning(vlcHost, vlcPort)
        stopRadioIfItsRunning // TODO
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
    
    // TODO
    private def stopRadioIfItsRunning { }
    
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













