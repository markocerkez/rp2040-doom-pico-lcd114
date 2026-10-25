# Doom on Raspberry Pi Pico + Waveshare Pico-LCD-1.14

Fork of [opensensor/rp2040-doom-PicoLCD](https://github.com/opensensor/rp2040-doom-PicoLCD)
(itself based on kilograham's rp2040-doom), with:

- GPIO button input for the Waveshare Pico-LCD-1.14 (joystick + A/B), see `src/pico/i_input.c`
- `NO_SOUND_HW=1` build option that never initialises audio (no I2S DAC needed), saves ~20 KB flash / ~15 KB RAM
- build fixes for pico-sdk 1.5.1 / arm-none-eabi-gcc 13

## Branches

- `main` / `no-sound` – audio disabled (recommended for the bare LCD board)
- `with-sound` – original audio path (needs an I2S DAC on GPIO 26/27/28)

## Ready-made firmware (`firmware/`)

Each `.uf2` contains the game **and** the shareware `doom1.whx` at `0x10041000`.
Hold BOOTSEL while plugging in the Pico, drag the file onto `RPI-RP2`.

| file | audio |
|------|-------|
| `doom-pico-lcd114-nosound.uf2` | off |
| `doom-pico-lcd114-sound.uf2`   | I2S on GPIO 26-28 |

## Controls

| input | action |
|-------|--------|
| joystick | move / turn |
| A | fire, select in menus |
| B | use / open doors, "yes" |
| joystick press | menu |

## Build

```
git clone -b 1.5.1 https://github.com/raspberrypi/pico-sdk   (+ git submodule update --init lib/tinyusb)
git clone -b sdk-1.5.1 https://github.com/raspberrypi/pico-extras
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=MinSizeRel -DPICO_SDK_PATH=../pico-sdk -DPICO_EXTRAS_PATH=../pico-extras -G Ninja ..
ninja doom_tiny_ST7789_240_135
```
The firmware must stay below 0x41000 bytes; combine it with `doom1.whx` into one UF2 (see `tools/make_uf2.py`).
