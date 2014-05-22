package utils

object MacUtils {

    def runningOnMac = {
        val osNameExists = System.getProperty("os.name").startsWith("Mac OS")
        val runningOnMac = if (!osNameExists) false else true
        runningOnMac
    }

}