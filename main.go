package main

import (
	"fmt"
	"os"
	"time"

	stopwatch "github.com/charmbracelet/bubbles/stopwatch"
	tea "github.com/charmbracelet/bubbletea"
)


type model struct {
	cursor int
	timer stopwatch.Model
	active string
	controls []string
	selected map[int]string
}

func initialModel() model {
	return model {
		controls: []string{"Toggle","Reset"},
		cursor: 0,
		active: "Stop",
		selected: make(map[int]string),
		timer: stopwatch.NewWithInterval(time.Second),
	}
}

func (m model) Init() tea.Cmd {
	return m.timer.Init() 
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "enter", " ":
			switch m.controls[m.cursor] {
			case "Toggle":
				if m.timer.Running() {
					m.active = "Start";
				} else {
					m.active = "Stop";
				}
				return m, m.timer.Toggle()
			case "Reset":
				return m, tea.Sequence(m.timer.Stop(), m.timer.Reset())
				
			}
		case "up", "k":
			if m.cursor > 0 {
				m.cursor--
			}
		case "down", "j":
			if m.cursor < len(m.controls)-1 {
				m.cursor++
			}
		}
	
	}
	var cmd tea.Cmd
	m.timer, cmd = m.timer.Update(msg)
	return m, cmd
}

func (m model) View() string {
	s := "Your timer:\n\n"

	for i, control := range m.controls {

	cursor := " "
		if m.cursor == i {
			cursor = ">"
		}

		s += fmt.Sprintf("%s %s\n", cursor, control)
	}
	s += "\n" + m.timer.View() + "\n"

	return s
}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Alas, there's been an error: %v", err)
        os.Exit(1)
    }
}