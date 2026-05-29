import time

class TuringMachineBinaryMultiplier:
    def __init__(self, tape_input):
        # Bandın esnekliği için soluna ve sağına yeterli miktarda Boşluk (B) ekliyoruz
        self.tape = list("BBB" + tape_input + "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
        self.head = 3  
        # Giriş karakterlerinin başladığı ilk indeks
        self.state = "q_init"
        self.transitions = {}
        self.step_count = 0
        self._generate_transition_matrix()

    def _generate_transition_matrix(self):
        """
        Turing Makinesi Geçiş Fonksiyonları Tanımı:
        Format: self.transitions[(mevcut_durum, okunan_sembol)] = (yeni_durum, yazılan_sembol, yön)
        Yön: 'R' (Sağ / Right), 'L' (Sol / Left)
        """
        # BAŞLANGIÇ VE OPERAND AYRIŞTIRMA
        # Çapa karakteri olan '*' bulunana kadar sağa doğru ilerle
        self.transitions[("q_init", "1")] = ("q_init", "1", "R")
        self.transitions[("q_init", "0")] = ("q_init", "0", "R")
        self.transitions[("q_init", "*")] = ("q_find_next_bit", "*", "R")

        # ÇARPAN BLOĞUNUN SONUNA ERİŞİM
        # İkinci sayının bittiği yer olan '=' işaretine kadar sağa git
        self.transitions[("q_scan_multiplier", "1")] = ("q_scan_multiplier", "1", "R")
        self.transitions[("q_scan_multiplier", "0")] = ("q_scan_multiplier", "0", "R")
        self.transitions[("q_scan_multiplier", "=")] = ("q_find_next_bit", "=", "L")

        # İŞLENECEK AKTİF BİTİN SEÇİLMESİ
        # Çarpan sayının sağından sola doğru 'A' (işlenmiş) olmayan ilk biti ara
        self.transitions[("q_find_next_bit", "A")] = ("q_find_next_bit", "A", "R")
        self.transitions[("q_find_next_bit", "1")] = ("q_process_1", "A", "L")
        self.transitions[("q_find_next_bit", "0")] = ("q_process_0", "A", "L")
        self.transitions[("q_find_next_bit", "=")] = ("q_accept", "=", "R")

        # SIFIR BİTİ OPERASYONU (Sadece Kaydırma)
        # Birinci sayıya dokunmadan en sağa sadece sıfır eklemek için konumlan
        for sym in ["A", "*"]:
            self.transitions[("q_process_0", sym)] = ("q_process_0", sym, "L")
            
        self.transitions[("q_process_0", "1")] = ("q_skip_multiplicand_0", "1", "L")
        self.transitions[("q_process_0", "0")] = ("q_skip_multiplicand_0", "0", "L")

        for sym in ["1", "0"]:
            self.transitions[("q_skip_multiplicand_0", sym)] = ("q_skip_multiplicand_0", sym, "L")
        self.transitions[("q_skip_multiplicand_0", "B")] = ("q_go_to_end_and_add_0", "B", "R")

        # BİR BİTİ OPERASYONU (Kopyalama ve Ekleme)
        # Birinci sayıyı kopyalamaya başlamak için sola yönlen
        for sym in ["A", "*"]:
            self.transitions[("q_process_1", sym)] = ("q_process_1", sym, "L")
            
        self.transitions[("q_process_1", "1")] = ("q_find_multiplicand_bit", "1", "N")
        self.transitions[("q_process_1", "0")] = ("q_find_multiplicand_bit", "0", "N")

        # Birinci sayının işlenmemiş sağ bitini oku, maskele (X veya Y yap)
        self.transitions[("q_find_multiplicand_bit", "X")] = ("q_find_multiplicand_bit", "X", "L")
        self.transitions[("q_find_multiplicand_bit", "Y")] = ("q_find_multiplicand_bit", "Y", "L")
        self.transitions[("q_find_multiplicand_bit", "1")] = ("q_add_1_to_res", "X", "R")
        self.transitions[("q_find_multiplicand_bit", "0")] = ("q_add_0_to_res", "Y", "R")
        self.transitions[("q_find_multiplicand_bit", "B")] = ("q_restore_multiplicand", "B", "R") 
        
        # VERİLERİ ŞERİDİN SAĞINA TAŞIMA VE YAZMA
        # Yol üzerindeki tüm karakterleri geçerek bandın en sağındaki boşluğa git
        for sym in ["1", "0", "*", "X", "Y", "=", "A"]:  
            self.transitions[("q_add_1_to_res", sym)] = ("q_add_1_to_res", sym, "R")
            self.transitions[("q_add_0_to_res", sym)] = ("q_add_0_to_res", sym, "R")
            self.transitions[("q_go_to_end_and_add_0", sym)] = ("q_go_to_end_and_add_0", sym, "R")

        # Boşluğa (B) ulaşıldığında değeri yaz ve döngüyü sürdürmek için geri dön
        self.transitions[("q_add_1_to_res", "B")] = ("q_return_left", "1", "L")
        self.transitions[("q_add_0_to_res", "B")] = ("q_return_left", "0", "L")
        self.transitions[("q_go_to_end_and_add_0", "B")] = ("q_return_to_multiplier", "0", "L")

        for sym in ["1", "0", "=", "A"]:
            self.transitions[("q_return_left", sym)] = ("q_return_left", sym, "L")
            self.transitions[("q_return_to_multiplier", sym)] = ("q_return_to_multiplier", sym, "L")
            
        self.transitions[("q_return_left", "*")] = ("q_find_multiplicand_bit", "*", "L")
        self.transitions[("q_return_to_multiplier", "*")] = ("q_find_next_bit", "*", "R")

        #  RESET VE MASKE ÇÖZME
        # Birinci sayıdaki geçici X ve Y işaretçilerini tekrar 1 ve 0 yap
        self.transitions[("q_restore_multiplicand", "X")] = ("q_restore_multiplicand", "1", "R")
        self.transitions[("q_restore_multiplicand", "Y")] = ("q_restore_multiplicand", "0", "R")
        self.transitions[("q_restore_multiplicand", "*")] = ("q_find_next_bit", "*", "R")

        # KAPANIŞ VE DOĞRULAMA
        self.transitions[("q_cleanup", "A")] = ("q_cleanup", "A", "R")
        self.transitions[("q_cleanup", "=")] = ("q_accept", "=", "R")

    def run_step(self):
        current_symbol = self.tape[self.head]
        state_key = (self.state, current_symbol)

        if state_key in self.transitions:
            next_state, write_symbol, direction = self.transitions[state_key]

            print(f"Adım {self.step_count:03d} | Durum: {self.state:<22} | Okunan: {current_symbol} | Yazılan: {write_symbol} | Yön: {direction}")
            self.display_tape()
            
            # Bandı ve kafayı güncelle
            self.tape[self.head] = write_symbol
            self.state = next_state
            
            if direction == 'R':
                self.head += 1
            elif direction == 'L':
                self.head -= 1
                
            self.step_count += 1
            return True
        else:
            return False

    def display_tape(self):
        # Görsel izleme için boşluk karakterlerini temizleyerek kafayı konumlandırıyoruz
        tape_visual = "".join(self.tape)
        pointer = " " * self.head + "^"
        print(f"Bant:  {tape_visual.replace('B', ' ')}")
        print(f"Kafa:  {pointer}")
        print("-" * 65)

    def extract_final_result(self):
        tape_str = "".join(self.tape)
        if "=" in tape_str:
            raw_res = tape_str.split("=")[1].replace("B", "").strip()
            if not raw_res or all(c == '0' for c in raw_res):
                return "0"
            return raw_res
        return "0"

def is_binary(input_str):
    return all(char in '01' for char in input_str) and len(input_str) > 0


# ANA PROGRAM AKIŞI
if __name__ == "__main__":
    print("=" * 65)
    print(" DETERMİNİSTİK TURING MAKİNESİ - İKİLİ ÇARPMA SİMÜLATÖRÜ")
    print("=" * 65)
    
    val1 = input("Çarpılan Sayıyı Giriniz (Multiplicand - Binary): ").strip()
    val2 = input("Çarpan Sayıyı Giriniz (Multiplier - Binary): ").strip()
    
    # Giriş Güvenlik Kontrolü
    if not (is_binary(val1) and is_binary(val2)):
        print("\n[HATA] Girdiler sadece '0' ve '1' içermelidir! Program sonlandırılıyor.")
    else:
        # Bant Formatlama Kuruluma Aktarılıyor (* ve = ekleme)
        formatted_tape = f"{val1}*{val2}="
        print(f"\nHazırlanan Başlangıç Bandı: {formatted_tape}\n")
        print("Simülasyon Başlatılıyor...\n" + "-" * 65)
        
        tm = TuringMachineBinaryMultiplier(formatted_tape)
        
        # Otomat döngüsü durma durumuna geçene kadar çalışır
        is_running = True
        while is_running:
            is_running = tm.run_step()
            
        if tm.state == "q_accept":
            binary_output = tm.extract_final_result()
            decimal_output = int(binary_output, 2)
            
            print("\n" + "=" * 65)
            print(" SİMÜLASYON BAŞARIYLA TAMAMLANDI (KABUL DURUMU) ")
            print("=" * 65)
            print(f"Metrik: Toplam {tm.step_count} adımsal geçiş yapıldı.")
            print(f"Binary Sonuç: {binary_output}")
            print(f"Decimal Karşılığı: {int(val1, 2)} x {int(val2, 2)} = {decimal_output}")
            print("=" * 65)
        else:
            print("\n[HATA] Turing Makinesi geçersiz dizilim saptadı (q_reject).")