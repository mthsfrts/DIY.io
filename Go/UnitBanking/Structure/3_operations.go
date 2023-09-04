package Structure

import (
	"fmt"
	"time"
)

// Estrutura
func NovaLista() *ListaContas {
	return &ListaContas{}
}

func (l ListaContas) InserirInicio(c Conta) {
	novoNo := &Node{Conta: c}
	if l.IsEmpty() {
		l.Head = novoNo
	} else {
		novoNo.Next = l.Head
		l.Head = novoNo
	}
}

func (l ListaContas) IsEmpty() bool {
	return l.Head == nil
}

func (l *ListaContas) Imprimir() bool {
	if l.Head == nil {
		// Se não houver contas, retorne false
		return false
	}

	curr := l.Head
	for curr != nil {
		fmt.Printf("Número da Conta: %d-%d, Saldo: %.2f\n", curr.Conta.Numero(), curr.Conta.Digito(), curr.Conta.Saldo())
		curr = curr.Next
	}
	return true
}

func (l *ListaContas) buscarNo(numero int, digito int) *Node {
	curr := l.Head
	for curr != nil {
		if curr.Conta.Numero() == numero && curr.Conta.Digito() == digito {
			return curr
		}
		curr = curr.Next
	}
	return nil
}

func (l *ListaContas) Buscar(numero int, digito int) Conta {
	no := l.buscarNo(numero, digito)
	if no != nil {
		return no.Conta
	}
	return nil
}

func (l *ListaContas) Remover(numero int, digito int) {
	if l.IsEmpty() {
		return
	}

	// Se a conta estiver na cabeça
	if l.Head.Conta.Numero() == numero && l.Head.Conta.Digito() == digito {
		l.Head = l.Head.Next
		return
	}

	prev := l.Head
	curr := l.Head.Next
	for curr != nil && (curr.Conta.Numero() != numero || curr.Conta.Digito() != digito) {
		prev = curr
		curr = curr.Next
	}

	if curr != nil {
		prev.Next = curr.Next
	}
}

func (l *ListaContas) Liberar() {
	l.Head = nil
}

// Interface
func (c *ContaGeral) Credito(valor float64) {
	c.saldo += valor
}

func (c *ContaGeral) Debito(valor float64) bool {
	if valor <= c.saldo {
		c.saldo -= valor
		return true
	}
	return false
}

func (c *ContaGeral) Render() float64 {
	if c.tipoConta == TipoContaNormal {
		return 0
	} else if c.tipoConta == TipoContaPoupanca {
		mesesDesdeCriacao := time.Now().Sub(c.dataCriacao).Hours() / 24 / 30
		taxaJuroAjustada := c.juros * (1 + 0.005*mesesDesdeCriacao)
		juros := c.saldo * taxaJuroAjustada
		c.Credito(juros)
		return juros
	} else if c.tipoConta == TipoContaFidelidade {
		mesesDesdeCriacao := time.Now().Sub(c.dataCriacao).Hours() / 24 / 30
		bonusAjustado := c.bonus * (1 + 0.007*mesesDesdeCriacao)
		bonusTotal := c.saldo * bonusAjustado
		c.Credito(bonusTotal)
		return bonusTotal
	}
	return 0
}

func (c *ContaGeral) Tipo() string {
	return c.tipoConta
}

func (c *ContaGeral) Numero() int {
	return c.numero
}

func (c *ContaGeral) Saldo() float64 {
	return c.saldo
}

func (c *ContaGeral) Digito() int {
	return c.digito
}

// Usuario
func (l *ListaContas) InserirContaGeral(numero int, digito int, saldoInicial float64, tipoconta string) *ContaGeral {
	if l.ContaExiste(numero, digito) {
		fmt.Println("Uma conta com esse número e dígito já existe!")
		return nil
	}

	taxajuros := 0.0
	taxarendimento := 0.0

	switch tipoconta {
	case TipoContaNormal:
		// Para contas correntes, os valores já estão configurados como 0
	case TipoContaPoupanca:
		taxajuros = TaxaJuroPoupanca
	case TipoContaFidelidade:
		taxarendimento = BonusFidelidade
	default:
		fmt.Println("Tipo de conta inválido!")
		return nil
	}
	conta := &ContaGeral{
		numero:    numero,
		saldo:     saldoInicial,
		tipoConta: tipoconta,
		juros:     taxajuros,
		bonus:     taxarendimento,
		digito:    digito,
	}
	l.InserirInicio(conta)

	return conta
}

func (l *ListaContas) Movimentacao(numero int, digito int, valor float64, tipo string, numeroDestino int, digitoDestino int) {
	conta := l.Buscar(numero, digito)
	if conta == nil {
		fmt.Println("Conta não encontrada!")
		return
	}

	switch tipo {
	case TipoMovimentacaoCredito:
		conta.Credito(valor)
		fmt.Printf("Novo saldo após crédito: %.2f\n", conta.Saldo())

	case TipoMovimentacaoDebito:
		conta.Debito(valor)
		fmt.Printf("Novo saldo após débito: %.2f\n", conta.Saldo())

	case TipoMovimentacaoTransferencia:
		if numeroDestino == 0 || digitoDestino == 0 {
			fmt.Println("Número ou dígito da conta de destino não fornecidos!")
			return
		}
		destino := l.Buscar(numeroDestino, digitoDestino)
		if destino == nil {
			fmt.Println("Conta de destino não encontrada!")
			return
		}
		if conta.Debito(valor) {
			destino.Credito(valor)
			fmt.Println("Transferência realizada com sucesso!")
		} else {
			fmt.Println("Saldo insuficiente para transferência!")
		}

	default:
		fmt.Println("Tipo de movimentação inválido!")
	}
}

func (l *ListaContas) ContaExiste(numeroConta int, digito int) bool {
	conta := l.Buscar(numeroConta, digito)
	return conta != nil
}

func (l *ListaContas) ConsultarSaldo(numero int, digito int) float64 {
	conta := l.Buscar(numero, digito)
	if conta != nil {
		return conta.Saldo()
	}
	fmt.Println("Conta não encontrada!")
	return -1
}

func (l *ListaContas) CalcularJuros() {
	// Verificar se a lista está vazia
	if l.Head == nil {
		fmt.Println("Não há contas cadastradas.")
		return
	}
	curr := l.Head
	for curr != nil {
		if cp, ok := curr.Conta.(*ContaGeral); ok {
			bonus := cp.Render()
			fmt.Printf("Juro rendendo para a conta %d. Valor do juros: %.2f\n", cp.Numero(), bonus)
		} else {
			fmt.Printf("A conta %d não é uma conta poupança e, portanto, não recebe juros, "+
				"ou voçê não possui Conta Poupança.\n", curr.Conta.Numero())
		}
		curr = curr.Next
	}
}

func (l *ListaContas) CalcularBonus() {
	// Verificar se a lista está vazia
	if l.Head == nil {
		fmt.Println("Não há contas cadastradas.")
		return
	}
	curr := l.Head
	for curr != nil {
		if cf, ok := curr.Conta.(*ContaGeral); ok {
			bonus := cf.Render()
			fmt.Printf("Bônus rendendo para a conta %d. Valor do bônus: %.2f\n", cf.Numero, bonus)
		} else {
			fmt.Printf("A conta %d não é uma conta fidelidade e, portanto, não recebe bônus, ou não possui "+
				"Conta Fidelidade.\n", curr.Conta.Numero())
		}
		curr = curr.Next
	}
}

func (l *ListaContas) ConsultarBonus(numero int, digito int) float64 {
	conta := l.Buscar(numero, digito)
	if cf, ok := conta.(*ContaGeral); ok {
		return cf.bonus
	}
	fmt.Println("Conta fidelidade não encontrada!")
	return -1
}
