%include header title="Ultimate Triad", user_status=user_status, base_url=base_url

<h2>Página de {{usuario.nombre}}</h2>
<center>
<form method="post" action="/subir_avatar" enctype="multipart/form-data">
	<table>
		<tr>
			<td class="tabla_usuario">Avatar</td>
		</tr>
		<tr>				
			<td class="tabla_usuario"><img src="/avatars/{{usuario.nombre}}.jpg" width="100" height="100"/></td>
		</tr>
		% if user_status["logged_in"] and user_status["current_user"].uid == usuario.uid:
		<tr>
			<td class="tabla_usuario"><input type="file" name="avatar" size="10"/></td>
		</tr>	
		<tr>
			<td class="tabla_usuario"><input type="submit" value="-Subir-"/></td>
		</tr>		
		%end
	</table>
</form>

<hr width="60%" />

<form method="post" action="/subir_mazo" enctype="multipart/form-data">	
	<table>
		<tr>
			<td class="tabla_usuario">Mazo</td>
		</tr>
		%info_mazo = be.obtener_mazo(usuario.nombre)
		%if not info_mazo:
			<p class="error">El usuario no tiene un mazo cargado en el sistema</p>
		%else:
			<tr>
				<td class="tabla_usuario"><a href="/usuario/{{usuario.uid}}/mazo">{{info_mazo[0]}}</a></td>
			</tr>
		%end
		% if user_status["logged_in"] and user_status["current_user"].uid == usuario.uid:		
			<tr>
				<td class="tabla_usuario"><input type="file" name="mazo" size="10"/></td>
			</tr>
			<tr>
				<td class="tabla_usuario"><input type="submit" value="-Subir Mazo-"/></td>
			</tr>
		%end
	</table>
</form>

% if user_status["logged_in"]:		
<hr width="60%" />
<center>
<a href="/lobby">Jugar</a> - <a href="/logout">Salir</a>
</center>
%end

%include footer

