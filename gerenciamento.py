from banco import *



@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    identifier = request.form.get("identificador")
    senha = request.form.get("senha")
    confim = request.form.get("confirmar_senha")
    usuario_existente = Usuario.query.filter_by(identificador=identifier).first()
    novo_usuario = Usuario(
                nome=nome,
                identificador=identifier,
                senha=generate_password_hash(senha)
            )

    if usuario_existente:
        return redirect(url_for('paginaprincipal'))
    print("SUCESSO")
    if senha != confim:
        return redirect(url_for('paginaprincipal'))
    db.session.add(novo_usuario)
    db.session.commit()
    session['usuario_id'] = novo_usuario.id
    return redirect(url_for('dashboard'))
    


@app.route("/login", methods=["POST"])
def login():
    identificador = request.form.get("identificador")
    senha_digitada = request.form.get("senha")
    usuario = Usuario.query.filter_by(identificador=identificador).first()
    if usuario and check_password_hash(usuario.senha, senha_digitada):
        session['usuario_id'] = usuario.id
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("paginaprincipal"))


@app.route("/transferir", methods=["POST"])
def transferir():
    chave = request.form.get("chave_destino")
    valor = float(request.form.get("valor"))
    remetente = Usuario.query.get(session['usuario_id'])
    destinatario = Usuario.query.filter_by(identificador=chave).first()
    if 'usuario_id' not in session:
        return redirect(url_for("paginaprincipal"))
    if not remetente:
        session.clear()
        return redirect(url_for("paginaprincipal"))
    if not destinatario or destinatario.id == remetente.id:
        return redirect(url_for("dashboard"))
    if valor <= 0 or remetente.saldo < valor:
        return redirect(url_for("dashboard"))
    remetente.saldo -= valor
    destinatario.saldo += valor
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/pix_credito", methods=["POST"])
def pixcredito():
    chave_destinopix = request.form.get("chave_destinopix")
    valorstr = float(request.form.get("valorpix"))
    if not valorstr:
        return redirect(url_for("dashboard"))
    valorpix = float(valorstr)
    remetentepix = Usuario.query.get(session['usuario_id'])
    destinatariopix = Usuario.query.filter_by(identificador=chave_destinopix).first()
    if 'usuario_id' not in session:
        return redirect(url_for("paginaprincipal"))
    if not remetentepix:
        session.clear()
        return redirect(url_for("paginalprincipal"))
    if not destinatariopix or destinatariopix.id == remetentepix.id:
        return redirect(url_for("dashboard"))
    if valorpix <= 0 or remetentepix.limite_credito < valorpix:
        return redirect(url_for("dashboard"))
    remetentepix.limite_credito -= valorpix 
    destinatariopix.saldo += valorpix
    remetentepix.fatura += valorpix + valorpix * 0.2
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/pagar_fatura", methods=["POST"])
def pgfatura():
    valor_pagamento = float(request.form.get("valor_pagamento"))
    usuariolocal = Usuario.query.get(session['usuario_id'])
    if 'usuario_id' not in session:
        return redirect(url_for("paginaprincipal"))
    if usuariolocal.saldo < valor_pagamento:
        return redirect(url_for("dashboard"))
        print("ta dando erro")
    if valor_pagamento <= -1:
        return redirect(url_for("dashboard"))
        print("ta dando erro")
    if usuariolocal.saldo >= valor_pagamento:
        usuariolocal.saldo -= valor_pagamento
        usuariolocal.fatura -= valor_pagamento
        usuariolocal.limite_credito += valor_pagamento
        db.session.commit()
        return redirect(url_for("dashboard"))
@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("paginaprincipal"))
        
with app.app_context():
    db.create_all()
