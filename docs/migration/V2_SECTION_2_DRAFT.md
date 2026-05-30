---
title: V2_SECTION_2_DRAFT
section: §2 — A Camada que Falta
version: 1.0
date: 2026-05-30
status: DRAFT — pending review and integration authorization
---

# §2 — A Camada que Falta

---

Uma camada de protocolo não é um produto. Não é uma aplicação. Não é uma API. Não é uma empresa.

Uma camada de protocolo é um conjunto de regras abertas — definidas por uma entidade de governança, publicadas para qualquer entidade ler, implementáveis por qualquer entidade que passe a certificação, e verificáveis por qualquer auditor que queira inspeccioná-las.

A distinção entre "protocolo" e "produto" é a distinção central de tudo o que se segue. Antes de definir o BANZA, é necessário compreender a diferença. Porque a maioria das pessoas que conhece sistemas de pagamento conhece produtos, não protocolos. E a maioria dos problemas que Angola tem no espaço dos pagamentos resulta precisamente de ter produtos onde deveria ter um protocolo.

---

## Uma analogia antes da finança

Considere as estradas.

A rede viária de Angola não pertence a nenhuma empresa de automóveis. As regras de circulação — sentido do trânsito, sinalização, limites de velocidade, dimensões máximas dos veículos — são definidas pelo Estado e aplicam-se a qualquer veículo, de qualquer fabricante, que circule nessa rede. A Toyota não é dona das estradas. A Chevrolet não é dona das estradas. Qualquer fabricante que produza veículos segundo as normas técnicas e legais pode vender automóveis que funcionam nessa infraestrutura.

O resultado é um ecossistema aberto: centenas de fabricantes, milhões de modelos, um conjunto único de regras partilhadas. A competição entre fabricantes é possível porque todos partilham a mesma infraestrutura.

Agora imagine um país onde cada fabricante de automóveis constrói a sua própria rede de estradas. A Toyota constrói estradas onde apenas circulam Toyotas. A Chevrolet constrói estradas onde apenas circulam Chevrolets. Um condutor que compra um Toyota tem acesso à rede Toyota. Se quiser aceder à rede Chevrolet, compra um Chevrolet. Os dois condutores, no mesmo país, não conseguem encontrar-se numa estrada comum.

Esse cenário absurdo é exactamente o que existe, hoje, nos pagamentos digitais angolanos. Cada rede é privada. Cada integração é proprietária. Um utilizador de uma carteira não consegue pagar a um utilizador de outra carteira — não porque seja tecnicamente impossível, mas porque não existe um conjunto de regras partilhadas que ambos os sistemas respeitem.

Um protocolo aberto de pagamentos é o equivalente à rede viária: regras públicas, certificação acessível, competição possível entre operadores.

---

## Dois modelos, dois resultados

A história dos pagamentos digitais no mundo demonstra que há dois modelos possíveis. O resultado de cada um é radicalmente diferente.

---

### O modelo fechado: M-Pesa

O M-Pesa é, por mérito próprio, um dos produtos financeiros mais transformadores que África alguma vez produziu. Lançado pela Safaricom no Quénia em 2007, expandiu o acesso financeiro a populações que nunca tinham tido conta bancária. Hoje opera em vários países africanos sob a Safaricom e a Vodacom.

O M-Pesa funciona assim: a Safaricom define as regras, opera a infraestrutura, e controla o acesso. Outras empresas podem integrar-se com o M-Pesa — através da API da Safaricom, mediante acordo com a Safaricom, nas condições definidas pela Safaricom. Não podem tornar-se operadores M-Pesa independentes. Não podem implementar o M-Pesa sem a Safaricom. A rede pertence ao operador.

Isto tem consequências directas:

- Quando a Safaricom decide alterar os preços das transacções, todos os comerciantes e utilizadores estão sujeitos a essa decisão.
- Quando a Safaricom decide encerrar o serviço num país, o serviço encerra.
- Uma startup que quer construir sobre o M-Pesa precisa de um acordo com a Safaricom — que pode ou não conceder, nas condições que decidir.

O M-Pesa é um produto extraordinário. Mas é um produto, não um protocolo. A rede pertence ao operador.

---

### O modelo aberto: Pix e UPI

O Pix e o UPI seguem um modelo diferente. Não é mais complexo — é estruturalmente diferente.

**Pix (Brasil, 2020).** O Banco Central do Brasil não criou um produto. Criou um protocolo: um conjunto de regras abertas para pagamentos instantâneos. Publicou as especificações. Abriu a certificação a bancos, fintechs e instituições de pagamento. O Nubank implementa o Pix. O Itaú implementa o Pix. O Google Pay implementa o Pix. Centenas de entidades implementam o Pix — cada uma com o seu produto, com a sua experiência de utilizador, com o seu modelo de negócio — mas todas segundo as mesmas regras abertas. Nenhuma delas é dona do Pix. Em dezoito meses, o Pix tornou-se o método de pagamento dominante no Brasil. A escala foi possível porque qualquer entidade podia participar.

**UPI (Índia, 2016).** A National Payments Corporation of India não criou um produto. Criou um protocolo. O PhonePe implementa o UPI. O Google Pay implementa o UPI. O Paytm implementa o UPI. Qualquer banco licenciado pode implementar o UPI. Nenhum deles é dono do UPI. Hoje, o UPI processa mil milhões de transacções mensais. A escala foi possível porque as regras são públicas e a certificação é acessível.

---

### A diferença estrutural

| | M-Pesa | Pix / UPI | BANZA |
|---|---|---|---|
| **Quem define as regras** | O operador (Safaricom/Vodacom) | Entidade de governança (BCB / NPCI) | Protocolo aberto (RFCs e ADRs) |
| **Quem pode participar** | Entidades com acordo com o operador | Qualquer entidade certificada | Qualquer entidade certificada |
| **Como se acede à especificação** | API proprietária, sob acordo | Especificação pública | Especificação pública |
| **Pode um terceiro tornar-se operador independente?** | Não | Sim | Sim |
| **Modelo de certificação** | Acordos bilaterais | Conformance suite aberto | Conformance suite aberto |

A diferença não é técnica. Não é sobre qual sistema é mais rápido ou mais barato. É sobre quem detém o controlo das regras — e, por consequência, quem tem acesso à infraestrutura.

No modelo fechado, o acesso à infraestrutura é uma concessão do operador dominante.

No modelo aberto, o acesso à infraestrutura é um direito de qualquer entidade que cumpra as regras.

---

## O que acontece se o Banzami desaparecer?

Esta pergunta é o teste definitivo.

No modelo fechado: se o operador principal desaparece, o sistema desaparece. O M-Pesa pertence à Safaricom. Se a Safaricom deixasse de operar o M-Pesa no Quénia amanhã, o sistema M-Pesa no Quénia desapareceria.

No modelo aberto: se um operador desaparece, os outros continuam. O Pix pertence ao protocolo, não ao Nubank. Se o Nubank desaparecesse amanhã, o Pix continuaria — porque o Itaú, o Bradesco, o Google Pay, e centenas de outros operadores continuariam a implementar o mesmo protocolo.

O BANZA segue o modelo aberto.

As regras do protocolo BANZA são públicas. Qualquer programador pode lê-las. A certificação é acessível — qualquer entidade que passe o conformance suite torna-se um operador certificado. O Banzami é o primeiro operador certificado e a implementação de referência. Mas não é o dono do protocolo. Não pode mudar as regras do protocolo unilateralmente. Não pode fechar o acesso à especificação.

Se o Banzami desaparecesse amanhã:

- As regras do protocolo BANZA continuariam a existir — são públicas, não pertencem ao Banzami.
- Os outros operadores certificados continuariam a operar — porque implementam o protocolo, não o produto do Banzami.
- A infraestrutura permaneceria — porque é protocolo, não produto.

Isto não é uma propriedade acidental do BANZA. É uma decisão de arquitectura deliberada. É o que separa infraestrutura de produto.

---

## Angola escolhe o modelo aberto

Angola tem as mesmas condições pré-existentes que o Brasil tinha em 2020 e a Índia tinha em 2016:

- Penetração crescente de smartphones
- Uma economia informal enorme com transacções diárias
- Vontade real de digitalizar o comércio
- Rails de liquidação interbancária já existentes (EMIS)
- Uma janela de oportunidade: a camada de protocolo ainda não existe

Angola tem também algo que o Brasil e a Índia não tinham nessa fase: a possibilidade de construir a camada de protocolo com uma década de aprendizagem sobre o que funcionou e o que não funcionou noutros mercados. Pular a fase das infraestruturas de cartão — que o Ocidente passou décadas a construir e que é inadequada para a economia angolana — e ir directamente para wallet-native, QR-first, liquidação instantânea por protocolo.

O BANZA é essa camada.

Não um produto. Não um operador. Não um banco. **Um protocolo** — para Angola, o que o Pix é para o Brasil e o UPI é para a Índia: regras abertas, certificação acessível, uma infraestrutura que nenhum operador pode fechar.

---

*Secção concluída. A próxima secção define o BANZA formalmente — a sua arquitectura, os seus princípios, e as suas distinções de identidade.*
