package utils

import java.net.Socket
import java.io.PrintWriter
import java.io.BufferedReader
import java.io.InputStreamReader

object NetworkUtils {

    /**
     * Sends the given command to the port the VLC server is running on.
     * Valid commands are "shutdown", "pause", "play", "seek +10", "voldown",
     * "volup", "volume +10".
     */
    def writeCommandToSocket(host: String, port: Int, command: String) {
        val socket = new Socket(host, port)
        val out = new PrintWriter(socket.getOutputStream, true)
        val in = new BufferedReader(new InputStreamReader(socket.getInputStream))
        out.println(command)
        socket.close
    }
        
}