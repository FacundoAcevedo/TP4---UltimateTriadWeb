%include header title="Ultimate Triad - Entrada", base_url=base_url

<h2>Bienvenido</h2>

<div style="width: 60%">
<p>Esta es la página principal del juego Ultimate Triad.  Aquí podrás
divertirte jugando contra otros jugadores a este espectacular juego.</p>
</div>

<div style="text-align: center;">
% if user_status["logged_in"]:
  Has ingresado como <a href="/usuario/{{user_status["current_user"].uid}}">{{user_status["current_user"].nombre}}</a>
  <a href="/logout">Salir</a>
% else:
  No has ingresado al sistema. Podés <a href="/login">Ingresar</a> o 
  <a href="/registrar">Registrarte</a>
% end
</div>

<hr width="60%" />
<center>
<p><a href="/lobby">Ver jugadores esperando y partidas en curso</a></p>
</center>
<hr width="60%" />

<p>
Antes de crear un mazo, revisá el listado de 
<a href="/cartas"><em>cartas oficiales</em></a>
</p>


%include footer
