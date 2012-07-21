%include header title="Registro", base_url=base_url

<br>

% if error:
	<p class="error">{{error}}</p>
% end
Ingresá el Nombre de usuario y una contraseña para unirte al sistema

<br><br>

<form method="post" action="/registrar">
	<center>
		<table>
			<tr>
				<td>Usuario</td>
				<td>
					<input type="text" name="username" size="10"/>
				</td>
			</tr>
			<tr>
				<td>Password:</td>
				<td>
					<input type="password" name="passwd" size="10"/>
				</td>
			</tr>
		</table>
	</center>
	<input type="submit" value="Registrate"/>
</form>

%include footer
