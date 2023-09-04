package Structure

import (
	"time"
)

type Node struct {
	Conta Conta
	Next  *Node
}

type ListaContas struct {
	Head *Node
	Tail *Node
}

type ContaGeral struct {
	numero      int
	digito      int
	saldo       float64
	dataCriacao time.Time
	tipoConta   string
	juros       float64
	bonus       float64
}

type Usuario struct {
	Nome   string
	Contas []*ContaGeral
}
