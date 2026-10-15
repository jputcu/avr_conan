#include <array>
#include <cstdint>
#include <avr/io.h>

// The freestanding libstdc++ and the avr-libc device headers together
int main() {
  constexpr std::array<std::uint8_t, 2> bits{_BV(PB0), _BV(PB1)};
  DDRB = bits[0] | bits[1];
  return 0;
}
