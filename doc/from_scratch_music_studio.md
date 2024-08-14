# From Scratch: Music Studio

## Location

## Building

## Sound Isolation

## Acoustics

### Psychoacoustics

## Monitor Speakers

- [ATC](https://atc.audio/professional)
- [Hot House](https://www.hothousepro.com)
- [Augspurger](https://augspurger.com)
- [PMC](https://pmc-speakers.com/studio/main-monitors)
- [Symphonic Acoustics (George Augspurger)](https://symphonicacoustics.com/george-augspurger-studio-monitors)
- [Quested](https://quested.com)

## Human Requirements

- Light
- HVAC

## Technical Requirements

### Signals

```mermaid
---
title: Studio Desktop & Laptop
---
flowchart LR
    Laptop <--> |Thunderbolt| LaptopDock[Dock]
    LaptopDock <--> |HDMI & USB| KVM[KVM Switch]
    LaptopDock <--> |Thunderbolt| LaptopInterface[Interface]

    %% KVM --> |HDMI| Display
    %% Mouse --> |USB| KVM
    %% Keyboard --> |USB| KVM

    Desktop[Desktop] <--> |Thunderbolt| DesktopDock[Dock]
    DesktopDock <--> |HDMI & USB| KVM
    Desktop <--> |Thunderbolt| DesktopInterface[Interface]

    %% AudioSource[Mic/Line] --> |Analog Audio| Converter
    Converter --> |Analog Audio| MonitorController[Monitor Controller]


    Converter[ADC/DAC] <--> |Ethernet| Dante
    LaptopInterface <--> |Ethernet| Dante[DANTE]
    DesktopInterface <--> |Ethernet| Dante

    MonitorController --> |Analog Audio| MainSpeaker[Main Speaker]
    MonitorController --> |Analog Audio| AltSpeaker[Alt Speaker]
```

- Electricity
- Analog
  - **Low**: Microphone
  - **Mid**: Line
  - **High**: Amp to speaker
- Digital
  - Ethernet
    - Video
    - Audio
      - AVB
      - DANTE
