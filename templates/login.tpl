%include header title="Entrar", user_status=user_status, base_url=base_url

<br>

% if error:
	<p class="error">{{error}}</p>
% end

Ingresá tu usuario y contraseña para poder entrar al sistema.

<br><br>

<form method="post" action="/login">
	<table>
	<tr>
		<td>Usuario</td>
		<td>
			<input type="text" name="username" size="10"/>
		</td>
	</tr>
	<tr>
		<td>Password</td>
		<td>
			<input type="password" name="passwd" size="10"/>
		</td>
	</tr>
	</table>
	<input type="submit" value="Entrar"/>
</form>

%include footer
