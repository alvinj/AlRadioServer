package controllers

import play.api._
import play.api.mvc._
import utils._

object Radio extends Controller {
  
    //
    // TODO get these from the config file
    //
    val host = "localhost"
    val port = 5150

    def index = Action {
        Ok(views.html.index("Welcome to AlRadio!"))
    }

    /**
     * Given an online stream name like "WGN", play its stream.
     */
    def playStream(streamName: String) = Action {
        println(s"STREAM NAME: $streamName")
        // if vlc player is playing, stop it
        // if radio is playing, stop it
        // start the vlc server with the given pls file
        val canonFilenameOption = getPlsCanonFilenameFromStreamName(streamName)
        canonFilenameOption match {
            case Some(canonFilename) =>
                println(s"CAME TO 'SOME'")
                // TODO send a proper ack to the client
                startVlcStreamServer(host, port, canonFilename)
                Ok("ack")
            case None => 
                println(s"CAME TO 'NONE'")
                // TODO send a proper ack to the client
                Ok("Error")
        }
        
    }
    
    def pauseVlc = Action {
        VlcUtils.pause(host, port)
        Ok("")
    }
    
    def playVlc = Action {
        VlcUtils.play(host, port)
        Ok("")
    }
    
    def shutdownVlc = Action {
        VlcUtils.shutdown(host, port)
        Ok("")
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













