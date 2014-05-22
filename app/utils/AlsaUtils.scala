package utils

/**
 * Utilities related to the Linux `alsa` commands.
 */
object AlsaUtils {
  
    /**
     * Takes an Int between 0 (mute) and 100 (full volume).
     * @return The exit code of the command that's executed.
     */
    def setVolume(volume: Int): Int = {
        if (MacUtils.runningOnMac) {
            0  // don't do anything when running on a mac dev system
        } else {
            import sys.process._
            val volumeCommand = play.Play.application.configuration.getString("volume_command")
            val adjustedVolume = getModifiedVolume(volume)
            val exitCode = s"$volumeCommand $adjustedVolume".!
            exitCode
        }
    }

    /**
     * TODO need some sort of scaled volume here.
     * there's a huge difference between something like 80 and 90.
     * can test with: for (i <- 0 to 100) println(getModifiedVolume(i))
     */
    def getModifiedVolume(volume: Int) = volume match {
        case x if 98 to 100 contains x => 100
        case x if 93 to 97 contains x => 97
        case x if 88 to 92 contains x => 94
        case x if 80 to 89 contains x => 91
        case x if 70 to 79 contains x => 88
        case x if 60 to 69 contains x => 85
        case x if 50 to 59 contains x => 82
        case x if 40 to 49 contains x => 76
        case x if 30 to 39 contains x => 70
        case x if 20 to 29 contains x => 60
        case x if 10 to 19 contains x => 50
        case x if 0 to   9 contains x => 0
    }
}







