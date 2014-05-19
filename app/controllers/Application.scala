package controllers

import play.api._
import play.api.mvc._

object Application extends Controller {

  def index = Action {
    val foo = play.Play.application.configuration.getString("foo")
    println(s"FOO = $foo")
    Ok(views.html.index("Your new application is ready."))
  }

}