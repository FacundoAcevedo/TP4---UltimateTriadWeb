%include header title="Ultimate Triad - Jugar", user_status=user_status, base_url=base_url

% jugando = False
% for id_jugador in 1,2:
	% jugador = jugadores[id_jugador-1]
	<div id="jugador{{id_jugador}}">
		<center>
		<img class="jugador" src="{{ base_url }}/avatars/{{jugador.obtener_nombre()}}.jpg"><br>
		{{jugador.obtener_nombre()}}<br><br>
		Mazo:
		<p class="mazo">{{jugador.obtener_nombre_mazo()}}</p>

		% if turno_jugador == id_jugador:
			% if user_status["logged_in"] and user_status["current_user"].nombre == jugador.obtener_nombre():
				% jugando = True
				<p><b>¡Es tu turno!</b></p>
			% else:
				<p>Es su turno</p>
			% end
		% end
		</center>
	</div>
% end
<div id="tablero">
	<form action="/jugar/{{id_partida}}" method="post">
		% for id_jugador in 1,2:
			% jugador = jugadores[id_jugador-1]
			% mano = jugador.obtener_mano()
			<div id="mano_jugador{{id_jugador}}">
			%if turno_jugador == id_jugador and jugando:
				%for x in range(len(mano)):
					<div id="carta_mano{{x}}">
						<input type="image" name="carta{{x}}" class="{{mano[x].obtener_estilo()}}" src="{{ base_url }}/static/cartas/{{mano[x].obtener_nombre()}}.png">
					</div>
				%end
			%else:
				%for x in range(len(mano)):
					<div id="carta_mano{{x}}">
						<br/>
					</div>
				%end
			%end
		</div>
	  % end
		<div id="cartas"><center>
			<table id="cartas">
				% for linea in ('A', 'B', 'C'):
					<tr class="linea_{{linea}">
					% for x in range(1,4):	
						<td >	
						%carta = tablero.obtener_carta(linea+str(x))
						%if not carta:
							% if jugando:
								<center><input type="radio" name="tablero" value="{{linea+str(x)}}"></center>
							% end
						%else:
							<img class="{{carta.obtener_estilo()}}" src="{{ base_url }}/static/cartas/{{carta.obtener_nombre()}}.png">
						%end
						</td>
					%end
					</tr>
				% end
			</table>
		</center></div>
	</form>
	%if ganador != "":
		<p class="ganar">Ha Ganado {{ganador}}</p>
	%end
</div>
<script type="text/javascript">
var turno = {{ turno_jugador }};
</script>
% if ganador == "" and ((not user_status["logged_in"]) or user_status["current_user"].nombre != jugadores[turno_jugador-1].obtener_nombre()):
<div style="display:none"><iframe src="/turno/{{id_partida}}"></iframe></div>
% end
%include footer
