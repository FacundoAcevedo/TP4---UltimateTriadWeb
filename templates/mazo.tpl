%include header title="Ultimate Triad - Mazo",base_url=base_url
<h2>{{mazo}}</h2>
<center>
	<table>
		<tr>
			<td class="encabezado">Carta</td>
			<td class="encabezado">Nombre</td>
		</tr>
		%for carta in cartas:	
			<tr>
				<td class="carta"><img class="carta_coleccion" src="{{ base_url }}/static/cartas/{{carta}}.png"></td>
				<td class="nombre">{{carta}}</td>
			</tr>
		%end		
	</table>
</center>

%include footer
