%include header title="Ultimate Triad - Entrar", base_url=base_url

<br>

% if error:
	<p class="error">{{error}}</p>
% end

<br>
<div style="text-align: right;width:60%">
% if user_status["logged_in"]:
  Has ingresado como <a href="/usuario/{{user_status["current_user"].uid}}">{{user_status["current_user"].nombre}}</a>.
  <a href="/logout">Salir</a>
<br/>
	% if user_status["current_user"].nombre not in esperando:
	<form method="post" action="/lobby/esperar">
		<input type="submit" value="Esperar para jugar" />
	</form>
	% else:
	<div style="display:none;"><iframe src="/lobby/esperando" height="0" frameborder="0"></iframe></div>
	% end
% else:
  No has ingresado al sistema. <a href="/login">Ingresar</a>
% end
</div>

<br>

	<center>
		<hr width="60%"/>
		% if esperando:
		<h3>Usuarios esperando para jugar</h3>
		<form method="post" action="/lobby/unir">
		<table cellspacing="5" >
			% for nombre in esperando:
			<tr>
				<td align="center"><img class="jugador" src="/avatars/{{nombre}}.jpg"><br />{{ nombre }}</td>
				<td valign="center">
				% if user_status["logged_in"] and nombre != user_status["current_user"].nombre:
					<input type="submit" value="Jugar" name="{{nombre}}"/>
				% end
				</td>
			</tr>
			% end
		</form>
		</table>
		% else:
		<h3>No hay usuarios esperando para jugar</h3>
		%end

		<hr width="60%"/>

		% if partidas:
		<h3>Partidas en curso:</h3>
		<table>
			% for id, partida in partidas.iteritems():
				% if partida.esta_activo():
			<tr>
				<td align="center"><img class="jugador"
					src="/avatars/{{partida.jugador1.obtener_nombre()}}.jpg"><br />{{ partida.jugador1.obtener_nombre() }}</td>
				<td valign="center">vs</td>
				<td align="center"><img class="jugador"
					src="/avatars/{{partida.jugador2.obtener_nombre()}}.jpg"><br />{{ partida.jugador2.obtener_nombre() }}</td>
				<td valign="center"><a href="/jugar/{{id}}">Ver</a></td>
			</tr>
				% end
			% end
		</table>
		% else:
		<h3>No hay partidas iniciadas</h3>
		%end
	</center>
</form>

%include footer
