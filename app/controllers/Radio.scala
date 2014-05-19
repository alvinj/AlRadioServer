package controllers

import play.api._
import play.api.mvc._
import org.apache.commons.exec._
import java.io.File
import utils._

object Radio extends Controller {
  
    val host = "localhost"
    val port = 5150

    def index = Action {
        val foo = play.Play.application.configuration.getString("foo")
        println(s"FOO = $foo")
        Ok(views.html.index("Your new application is ready."))
    }

    private def startVlcServer {

        //
        // TODO working here ...
        //
        val cmd = VlcUtils.buildVlcStreamServerCommand("localhost", 5150, "mac.pls")
        val watchDog = new ExecuteWatchdog(ExecuteWatchdog.INFINITE_TIMEOUT)
    
        // result handler for executing the process in a async way
        val resultHandler = new DefaultExecuteResultHandler
    
        // using stdout for the output/error stream
        val streamHandler = new PumpStreamHandler
    
        //This is used to end the process when the JVM exits
        val processDestroyer = new ShutdownHookProcessDestroyer
    
        //Our main command executor
        val executor = new DefaultExecutor
    
        //Setting the properties
        executor.setStreamHandler(streamHandler)
        executor.setWatchdog(watchDog)
    
        //Setting the working directory
        //Use of recursion along with the ls makes this a long running process
        // executor.setWorkingDirectory(new File("/Users/Al/Projects/Scala/Tests/ApacheExec"))
        executor.setProcessDestroyer(processDestroyer)
    
        //Executing the command
        executor.execute(cmd, resultHandler)
        println("*** immediately after 'execute' ***")
    
        // execution stops with this statement (until the command returns)
        resultHandler.waitFor
        println("*** immediately after 'waitFor' ***")
    
        val exitValue = resultHandler.getExitValue
        println(exitValue)
    
        if (executor.isFailure(exitValue)) {
          System.out.println("Execution failed")
        } else {
          System.out.println("Execution Successful")
        }

    }
    

}













