// Ajusta estos valores a tu negocio.
export const config = {
  timezone: "Europe/Madrid",
  // 0 = domingo ... 6 = sábado. null = cerrado.
  horario: {
    0: null,
    1: ["09:00", "18:00"],
    2: ["09:00", "18:00"],
    3: ["09:00", "18:00"],
    4: ["09:00", "18:00"],
    5: ["09:00", "14:00"],
    6: null,
  },
  duracionMinutos: 30,
  diasMaximosVista: 14,
};
