%include header title="Ultimate Triad - Cartas",base_url=base_url

<center>
	<table>
		<tr>
			<td class="encabezado">Carta</td>
			<td class="encabezado">Nombre</td>
			<td class="encabezado">Norte</td>
			<td class="encabezado">Sur</td>
			<td class="encabezado">Este</td>
			<td class="encabezado">Oeste</td>
		</tr>
		%for carta in cartas:	
			<tr>
				<td class="carta"><img class="carta_coleccion" src="{{ base_url }}/static/cartas/{{carta[0]}}.png"></td>
				<td class="nombre">{{carta[0]}}</td>
				<td class="atributo">{{carta[1]}}</td>
				<td class="atributo">{{carta[2]}}</td>
				<td class="atributo">{{carta[3]}}</td>
				<td class="atributo">{{carta[4]}}</td>
			</tr>
		%end		
	</table>
</center>

%include footer
