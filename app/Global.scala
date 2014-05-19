import play.api._

import scala.collection.JavaConversions._

object Global extends GlobalSettings {

  override def onStart(app: Application) {
      Logger.info("Application has started")
      val foo = play.Play.application.configuration.getString("foo")
      println(s"FOO = $foo (STARTUP)")
      val fooBar = play.Play.application.configuration.getString("bar.baz")
      println(s"fooBar = ${fooBar} (STARTUP)")

      // the list of stations (99.5, 102.3, etc.)
      play.Play.application.configuration.getDoubleList("stations").foreach { station =>
          println(s"STATION: $station")
      }
      
      // the list of streams ("104.3" is "104_3.pls", etc.)
      play.Play.application.configuration.getConfigList("streams") foreach { stream =>
          println(s" ${stream.getString("name")} is ${stream.getString("file")}")
      }
  }

  override def onStop(app: Application) {
      Logger.info("Application shutdown...")
  }  
    
}