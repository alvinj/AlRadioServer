package controllers

import play.api._
import play.api.mvc._
import utils._

object Radio extends Controller {
  
    //
    // TODO move this to the Global object?
    //
    val host = "localhost"
    val port = 5150

    def index = Action {
        val foo = play.Play.application.configuration.getString("foo")
        println(s"FOO = $foo")
        Ok(views.html.index("Your new application is ready."))
    }

    def playStream(plsFile: String) = Action {
        // if vlc player is playing, stop it
        // if radio is playing, stop it
        // start the vlc server with the given pls file
        Ok("Coming soon")
    }

    /**
     * Start a stream, like "wgn.pls" or "104_3.pls".
     */
    private def startVlcStreamServer(plsFile: String) {

        //
        // TODO working here ...
        //
        val cmd = VlcUtils.buildVlcStreamServerCommand("localhost", 5150, "mac.pls")
    }
    
    

}













