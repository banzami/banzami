# BANZA — Manifesto do Protocolo

> This document describes: **BANZA** — the open financial infrastructure protocol.
> For other layers: [BanzAI](../banzai/BANZAI_REFERENCE.md) · [the reference operator](../banza/BANZA_REFERENCE.md)

**Version:** 1.0  
**Date:** 2026-05-30  
**Status:** Official  
**Authority:** ADR-025

---

## O Problema: Angola Tem as Peças

Angola tem bancos. Vinte e três instituições financeiras licenciadas. Um sistema de liquidação interbancária — o EMIS. Redes de caixas automáticos. Aplicações de homebanking. O Multicaixa. Dezasseis milhões de pessoas com telemóvel.

Angola tem as peças. O que Angola não tem é a camada que as conecta.

### O que existe não é suficiente

Para integrar pagamentos, uma empresa tem de estabelecer um acordo bilateral com um banco. O processo pode demorar meses. A documentação é privada. Os termos são negociados caso a caso. O acesso é discricionário — não existe um conjunto de regras públicas que qualquer entidade possa ler e implementar.

Para processar pagamentos de forma independente, uma fintech tem de se tornar banco. Para que carteiras de operadores diferentes comuniquem entre si, não existe mecanismo — cada rede é fechada sobre si mesma.

### Os sintomas visíveis

**Comprovativo por WhatsApp.** Capturas de ecrã de transferências bancárias como prova de pagamento — porque não existe alternativa com garantia de protocolo.

**Integração fechada.** Uma empresa integra-se com o sistema de um banco específico. Essa integração não funciona com outro banco. Não existe uma interface standard que qualquer banco respeite — porque não existe um protocolo que o exija.

**Exclusão da pequena empresa.** Um terminal POS exige contrato de aquisição, hardware e taxas mensais. Uma mercearia de bairro não tem condições.

**Dependência de redes proprietárias.** Cada plataforma funciona segundo as suas próprias regras. Um operador pode alterar taxas, desligar funcionalidades, ou encerrar sem aviso.

**Ausência de garantias de protocolo.** A liquidação instantânea é uma promessa contratual — não um invariante verificável por auditores independentes.

### A causa

Angola tem rails de liquidação — o EMIS resolve o movimento final entre bancos. Não resolve: quem pode aceder ao sistema de pagamentos, em que condições, e segundo que regras verificáveis.

Esta camada tem um nome: **camada de protocolo**.

> Esse é o vazio que o BANZA preenche. Não como banco. Não como produto fintech. Como protocolo.

---

## A Camada que Falta

Uma camada de protocolo não é um produto. Não é uma aplicação. Não é uma empresa. É um conjunto de regras abertas — definidas por um processo de governança, publicadas para qualquer entidade ler, implementáveis por qualquer entidade que passe a certificação.

### Dois modelos

**O modelo fechado: M-Pesa**

O M-Pesa pertence à Safaricom. As regras são do operador. Quando a Safaricom decide alterar preços, todos os utilizadores ficam sujeitos. Uma startup que quer construir sobre o M-Pesa precisa de um acordo nas condições que o operador decidir.

O M-Pesa é um produto extraordinário. Mas é um produto — não um protocolo. A rede pertence ao operador.

**O modelo aberto: Pix e UPI**

O Banco Central do Brasil não criou um produto — criou um protocolo. O Nubank implementa o Pix. O Itaú implementa o Pix. O Google Pay implementa o Pix. Centenas de entidades implementam o Pix — cada uma com o seu produto, a sua experiência, o seu modelo de negócio — mas todas segundo as mesmas regras abertas. Nenhuma delas é dona do Pix.

Em menos de dois anos, o Pix tornou-se o método de pagamento mais utilizado no Brasil.

A India Payments Corporation seguiu o mesmo modelo com o UPI em 2016. Em 2024, o UPI processava mais de 15 mil milhões de transacções mensais.

### A diferença estrutural

| | M-Pesa | Pix / UPI | BANZA |
|---|---|---|---|
| **Quem define as regras** | O operador | Entidade de governança | Protocolo aberto (RFCs e ADRs) |
| **Quem pode participar** | Entidades com acordo com o operador | Qualquer entidade certificada | Qualquer entidade certificada |
| **Pode um terceiro tornar-se operador independente?** | Não | Sim | Sim |

### O teste definitivo: o que acontece se o operador desaparecer?

No modelo fechado: se o operador principal desaparece, o sistema desaparece.

No modelo aberto: se um operador desaparece, os outros continuam. O Pix não pertence ao Nubank. Se o Nubank desaparecesse amanhã, o Pix continuaria.

**O BANZA segue o modelo aberto.**

As regras do protocolo BANZA são públicas. O operador é o primeiro operador certificado e a implementação de referência — mas não é o dono do protocolo. Se o operador desaparecesse amanhã: as regras do protocolo BANZA continuariam a existir. Os outros operadores certificados continuariam a operar. A infraestrutura permaneceria.

Isto não é uma propriedade acidental. É uma decisão de arquitectura deliberada.

---

## O que é o BANZA

O BANZA é o protocolo aberto de pagamentos digitais que Angola não tinha — a camada de infraestrutura certificada que qualquer programador, operador ou instituição pode implementar.

### Quatro propriedades concretas

**Regras públicas.** A especificação do BANZA — os RFCs, os ADRs, o conformance suite — está disponível para qualquer programador ler, qualquer operador implementar, e qualquer auditor inspeccionar. Nenhuma documentação está fechada atrás de um acordo de confidencialidade.

**Certificação aberta.** Qualquer entidade legal que passe o conformance suite torna-se um operador certificado BANZA. Não existe processo de acreditação institucional. Não existe acordo bilateral. O acesso à certificação é definido pelas regras do protocolo.

**Invariantes verificáveis.** As propriedades financeiras do protocolo são impostas pelo kernel e verificáveis por qualquer auditor independentemente de qualquer operador. A liquidação em T+0 é um invariante do kernel Rust: o código não pode completar uma transacção que viole esta propriedade.

**Federação.** Operadores certificados podem encaminhar pagamentos entre si sem acordos bilaterais — porque ambos implementam o mesmo protocolo aberto.

### O que o BANZA não é

| O BANZA não é | Porquê a distinção importa |
|---|---|
| **Um banco** | O BANZA define regras que operadores seguem. Não detém dinheiro de ninguém. |
| **Um produto fintech** | Um produto pertence ao seu operador. O protocolo pertence à infraestrutura. |
| **Uma API fechada** | A especificação do BANZA é pública. Nenhum operador pode alterá-la unilateralmente. |
| **O operador** | O operador é um operador — o primeiro e a implementação de referência. Não é o protocolo. |

---

## Os Quatro Princípios do Protocolo

Qualquer operador certificado BANZA implementa estes quatro princípios. Não são funcionalidades de nenhum operador. São invariantes do protocolo — propriedades que qualquer implementação deve garantir para ser certificada.

| Princípio | O que o protocolo garante |
|---|---|
| **Wallet-native** | Cada conta é uma carteira. Pagamentos são transferências directas — sem IBAN, sem intermediário de liquidação adicional. |
| **QR-native** | O QR é a superfície primária de pagamento definida pelo protocolo. Um operador certificado que não exponha a superfície QR não está em conformidade. |
| **Programmable** | A integração programática via SDK é um requisito do protocolo — não uma funcionalidade opcional. |
| **Instant settlement** | A liquidação em T+0 é um invariante do protocolo — verificável no kernel, não dependente da política de nenhum operador. |

---

## A Distinção Fundamental: Protocolo ≠ Operador

O protocolo define as regras. O operador implementa-as.

O protocolo existe independentemente de qualquer operador. Se todos os operadores actuais desaparecessem amanhã, o protocolo — as regras, a especificação, o conformance suite — continuaria a existir.

A relação é exactamente a que existe entre o Pix e o Nubank. O Nubank é o maior utilizador do Pix no Brasil — mas o Pix não pertence ao Nubank.

---

## O Nome

**Banza** e **the reference operator** são palavras enraizadas nas tradições linguísticas bantu de Angola, especialmente no universo Kikongo, onde *mbanza* designa um lugar de encontro — um centro de vida comunitária. Nomes distintamente angolanos — não palavras emprestadas de outro continente.

---

## Declaração de Visão

O ecossistema de pagamentos digitais de Angola será construído sobre o protocolo BANZA — não sobre o produto de um único operador.

O ecossistema tem sucesso quando:
- Qualquer programador pode construir sobre o protocolo
- Qualquer operador pode certificar-se
- Qualquer angolano pode transaccionar, independentemente de qual operador usa

**O protocolo é o que fica.**

Os operadores mudam. Os produtos evoluem. O que o BANZA garante é que as regras permaneçam abertas, a certificação permaneça acessível, e a infraestrutura permaneça de Angola.

> **BANZA é o protocolo. BANZA move o dinheiro. O protocolo existe independentemente de qualquer operador.**

---

**Referências:**

- ADR-025 — Hierarquia canónica de três níveis (supersede ADR-016)
- ADR-014 — Angola national mission
- ADR-018 — Open financial kernel
- ADR-019 — Operator separation
- ADR-024 — Reference operator

Ver também:
- [BANZA_REFERENCE.md](BANZA_REFERENCE.md) — Canonical protocol reference (rules, invariants, governance, certification)
- [BANZA_GOVERNANCE.md](BANZA_GOVERNANCE.md) — Protocol governance model
- [BANZAI_REFERENCE.md](../banzai/BANZAI_REFERENCE.md) — Protocol Operating System
- [BANZA_REFERENCE.md](../banza/BANZA_REFERENCE.md) — Reference operator
