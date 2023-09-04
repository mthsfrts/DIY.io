package Structure

type Conta interface {
	Credito(valor float64)
	Debito(valor float64) bool
	Saldo() float64
	Numero() int
	Digito() int
}
