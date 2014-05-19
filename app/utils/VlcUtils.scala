package utils

import org.apache.commons.exec.CommandLine

object VlcUtils {

    /**
     * Call like "startVlcStreamServer('localhost', 5150, 'wgn.pls')"
     * plsFile - like "wgn.pls", "104_3.pls", etc. 
     */
    def buildVlcStreamServerCommand(host: String, port: Int, plsFile: String): CommandLine = {      
        if (runningOnMac) {
            buildVlcServerCommandMac(plsFile, host, port)
        } else {
            buildVlcServerCommandRpi(plsFile, host, port)
        }
    }
    
    private def buildVlcServerCommandMac(fileOrStream: String, host: String, port: Int) = {
        val cmd = new CommandLine(getVlcServerCommand)
        cmd.addArgument(fileOrStream)
        cmd.addArgument("--rc-host")
        cmd.addArgument(s"${host}:${port}")
        cmd.addArgument("-I")
        cmd.addArgument("dummy")
        cmd.addArgument("-I")
        cmd.addArgument("rc")
        cmd
    }
    
    private def buildVlcServerCommandRpi(fileOrStream: String, host: String, port: Int) = {
        val cmd = new CommandLine(getVlcServerCommand)
        cmd.addArgument(fileOrStream)
        cmd.addArgument("--rc-host")
        cmd.addArgument(s"${host}:${port}")
        cmd.addArgument("-I")
        cmd.addArgument("dummy")
        cmd.addArgument("-I")
        cmd.addArgument("rc")
        cmd
    }
    
    private def getVlcServerCommand: String = {      
        if (runningOnMac) {
            "/Applications/VLC.app/Contents/MacOS/VLC"
        } else {
            "vlc"
        }
    }
    
    private def runningOnMac = {
        val mrjVersionExists = System.getProperty("mrj.version") != null
        val osNameExists = System.getProperty("os.name").startsWith("Mac OS")
        val runningOnMac = if (!mrjVersionExists || !osNameExists) false else true
        runningOnMac
    }

}