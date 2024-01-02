package main

import (
	"fmt"
	"os"
	"time"

	stopwatch "github.com/charmbracelet/bubbles/stopwatch"
	tea "github.com/charmbracelet/bubbletea"
	lipgloss "github.com/charmbracelet/lipgloss"
)


type model struct {
	cursor int
	timer stopwatch.Model
	controls []string
	actions []string
	selected map[int]string
}

var modelStyle = lipgloss.NewStyle().
					Width(50).
					Height(5).
					Align(lipgloss.Center, lipgloss.Center).
					BorderStyle(lipgloss.NormalBorder()).
					// Foreground(lipgloss.Color("229")).
					Background(lipgloss.Color("#3C3C32")).
					BorderForeground(lipgloss.Color("9"))


func initialModel() model {
	return model {
		controls: []string{"Toggle","Reset"},
		actions: []string{"Stop","Reset"},
		cursor: 0,
		selected: make(map[int]string),
		timer: stopwatch.NewWithInterval(time.Millisecond),
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
					m.actions[0] = "Start"
				} else {
					m.actions[0] = "Stop"
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
	s := "Stopwatch:\n\n"


	for i, control := range m.actions{

	cursor := " "
		if m.cursor == i {
			cursor = ">"
		}

		s += fmt.Sprintf("%s %s\n", cursor, control)
	}

	s += "\n" 
	s += lipgloss.PlaceHorizontal(20, lipgloss.Center, time.Duration.String((m.timer.Elapsed())),lipgloss.WithWhitespaceBackground(lipgloss.Color("29")))


	return modelStyle.Render(s)

}

func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Alas, there's been an error: %v", err)
        os.Exit(1)
    }
}