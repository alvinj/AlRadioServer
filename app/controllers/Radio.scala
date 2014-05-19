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
    val host = play.Play.application.configuration.getString("host")
    val port = play.Play.application.configuration.getInt("port")

    def index = Action {
        Ok(views.html.index("Welcome to AlRadio!"))
    }

    /**
     * Given an online stream name like "WGN", play its stream.
     */
    def playStream(streamName: String) = Action {
        shutdownVlcIfItsRunning(host, port)
        stopRadioIfItsRunning // TODO
        val canonFilenameOption = getPlsCanonFilenameFromStreamName(streamName)
        val result = startVlcServerWithPlsFile(canonFilenameOption)
        result
    }
    
    private def startVlcServerWithPlsFile(canonFilenameOption: Option[String]) = {
        canonFilenameOption match {
            case Some(canonFilename) =>
                startVlcStreamServer(host, port, canonFilename)
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
        VlcUtils.pause(host, port)
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    def playVlc = Action {
        VlcUtils.play(host, port)
        Ok(Json.toJson(Map("success" -> toJson(true), "msg" -> toJson("ack"))))
    }
    
    def shutdownVlc = Action {
        VlcUtils.shutdown(host, port)
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













