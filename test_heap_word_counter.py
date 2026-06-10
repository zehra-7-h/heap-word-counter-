#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UNITTEST - Heap Word Counter Proje Testleri

Bu dosya, heap_word_counter.py programının tüm fonksiyonlarını test eder.
Unittest modülü kullanılmıştır.

Çalıştırmak için:
    python -m unittest test_heap_word_counter.py -v
    veya
    python test_heap_word_counter.py
"""

import unittest
import os
import tempfile
import sys
from io import StringIO
from heap_word_counter import DualKeyHeap, read_and_process_file


class TestDualKeyHeap(unittest.TestCase):
    """DualKeyHeap sınıfının testleri"""
    
    def setUp(self):
        """Her test öncesi çalışan setup metodu"""
        self.heap = DualKeyHeap()
    
    def test_init(self):
        """Heap başlatma testı"""
        self.assertEqual(len(self.heap.word_counts), 0)
        self.assertEqual(len(self.heap.heap), 0)
        self.assertIsInstance(self.heap.word_counts, dict)
        self.assertIsInstance(self.heap.heap, list)
    
    def test_add_single_word(self):
        """Tek kelime ekleme testı"""
        self.heap.add_word("Ankara")
        self.assertEqual(self.heap.word_counts["ankara"], 1)
    
    def test_add_multiple_same_words(self):
        """Aynı kelimeyi birden fazla kez ekleme testı"""
        self.heap.add_word("Ankara")
        self.heap.add_word("Ankara")
        self.heap.add_word("ankara")  # Farklı harf ama aynı kelime
        self.assertEqual(self.heap.word_counts["ankara"], 3)
    
    def test_add_different_words(self):
        """Farklı kelimeler ekleme testı"""
        self.heap.add_word("Ankara")
        self.heap.add_word("Konya")
        self.heap.add_word("Van")
        self.assertEqual(len(self.heap.word_counts), 3)
    
    def test_case_insensitivity(self):
        """Büyük/küçük harf duyarlılığı testı"""
        self.heap.add_word("Ankara")
        self.heap.add_word("ANKARA")
        self.heap.add_word("ankara")
        self.assertEqual(self.heap.word_counts["ankara"], 3)
    
    def test_build_heap(self):
        """Heap oluşturma testı"""
        self.heap.add_word("Ankara")
        self.heap.add_word("Ankara")
        self.heap.add_word("Konya")
        self.heap.add_word("Adana")
        self.heap.add_word("Adana")
        self.heap.add_word("Adana")
        
        self.heap.build_heap()
        
        # Heap boş olmamalı
        self.assertGreater(len(self.heap.heap), 0)
    
    def test_get_sorted_output(self):
        """Sıralı çıktı testı"""
        self.heap.add_word("Ankara")
        self.heap.add_word("Ankara")
        self.heap.add_word("Konya")
        self.heap.add_word("Adana")
        self.heap.add_word("Adana")
        self.heap.add_word("Adana")
        
        self.heap.build_heap()
        output = self.heap.get_sorted_output()
        
        # Çıktı bir liste olmalı
        self.assertIsInstance(output, list)
        
        # Her eleman 3 parçalı tuple olmalı
        for item in output:
            self.assertEqual(len(item), 3)
            letter, word, count = item
            self.assertIsInstance(letter, str)
            self.assertIsInstance(word, str)
            self.assertIsInstance(count, int)
    
    def test_alphabetical_sorting(self):
        """Alfabetik sıralama testı"""
        self.heap.add_word("Van")
        self.heap.add_word("Ankara")
        self.heap.add_word("Konya")
        self.heap.add_word("Adana")
        
        self.heap.build_heap()
        output = self.heap.get_sorted_output()
        
        # İlk harfleri kontrol et
        letters = [item[0] for item in output]
        self.assertEqual(sorted(letters), letters)  # Sıralı olmalı
    
    def test_count_sorting_within_letter(self):
        """Aynı harfde sayıya göre sıralama testı"""
        # A harfi ile başlayan kelimeler
        self.heap.add_word("Adana")
        self.heap.add_word("Adana")
        self.heap.add_word("Adana")  # 3 kez
        
        self.heap.add_word("Ankara")
        self.heap.add_word("Ankara")  # 2 kez
        
        self.heap.add_word("Avi")    # 1 kez
        
        self.heap.build_heap()
        output = self.heap.get_sorted_output()
        
        # A ile başlayan kelimeleri al
        a_words = [item for item in output if item[0] == 'A']
        
        # Sayıları kontrol et (yüksekten düşüğe)
        counts = [item[2] for item in a_words]
        self.assertEqual(counts, sorted(counts, reverse=True))
    
    def test_empty_heap(self):
        """Boş heap testı"""
        self.heap.build_heap()
        output = self.heap.get_sorted_output()
        self.assertEqual(len(output), 0)
    
    def test_single_letter_words(self):
        """Tek harfli kelimeler testı"""
        self.heap.add_word("a")
        self.heap.add_word("A")
        
        self.heap.build_heap()
        self.assertEqual(self.heap.word_counts["a"], 2)
    
    def test_word_with_numbers(self):
        """Sayı içeren kelimeler testı (add_word açısından)"""
        # add_word sadece kelimeleri kabul eder, sayıları değil
        # Ama eğer sayı içeren string gönderirse?
        self.heap.add_word("Test123")
        # Sayısal olmayan kısım işlenir
        self.assertGreater(len(self.heap.word_counts), 0)
    
    def test_duplicate_prevention(self):
        """Aynı kelimenin birden fazla kez sayılması testı"""
        words = ["Ankara", "ankara", "ANKARA"]
        for word in words:
            self.heap.add_word(word)
        
        # Benzersiz kelime sayısı 1 olmalı
        self.assertEqual(len(self.heap.word_counts), 1)
    
    def test_output_count_sum(self):
        """Çıktıdaki sayıların toplamı testı"""
        self.heap.add_word("Test")
        self.heap.add_word("Test")
        self.heap.add_word("Test")
        
        self.heap.build_heap()
        output = self.heap.get_sorted_output()
        
        total_count = sum(item[2] for item in output)
        self.assertEqual(total_count, 3)
    
    def test_large_dataset(self):
        """Büyük veri seti testı"""
        # 1000 kelime ekle
        for i in range(100):
            self.heap.add_word("Ankara")
        for i in range(50):
            self.heap.add_word("Konya")
        for i in range(75):
            self.heap.add_word("Van")
        
        self.heap.build_heap()
        output = self.heap.get_sorted_output()
        
        # 3 benzersiz kelime olmalı
        self.assertEqual(len(output), 3)
        
        # Sayılar doğru olmalı
        counts = {item[1]: item[2] for item in output}
        self.assertEqual(counts["ankara"], 100)
        self.assertEqual(counts["konya"], 50)
        self.assertEqual(counts["van"], 75)


class TestFileProcessing(unittest.TestCase):
    """Dosya işleme testleri"""
    
    def setUp(self):
        """Test dosyaları oluştur"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Test dosyalarını sil"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_read_simple_file(self):
        """Basit dosya okuma testı"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Ankara Konya Ankara")
        
        heap = read_and_process_file(test_file)
        self.assertEqual(len(heap.word_counts), 2)
    
    def test_read_file_with_uppercase(self):
        """Büyük harfler testı"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("ANKARA Konya ankara")
        
        heap = read_and_process_file(test_file)
        # "ankara" 2 kez (ANKARA ve ankara), "konya" 1 kez
        self.assertEqual(heap.word_counts["ankara"], 2)
        self.assertEqual(heap.word_counts["konya"], 1)
    
    def test_read_file_with_punctuation(self):
        """Noktalama işaretleri testı"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Ankara, Konya. Ankara!")
        
        heap = read_and_process_file(test_file)
        # Noktalamalar kaldırılmalı
        self.assertEqual(heap.word_counts["ankara"], 2)
    
    def test_read_file_with_numbers(self):
        """Sayılar testı"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Ankara 123 Konya 456 Ankara")
        
        heap = read_and_process_file(test_file)
        # Sayılar görmezden gelinmeli
        self.assertEqual(len(heap.word_counts), 2)
    
    def test_read_file_with_special_chars(self):
        """Özel karakterler testı"""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Ankara@Konya#Ankara$")
        
        heap = read_and_process_file(test_file)
        # Kelimelerin ayrı ayrı ele alınması gerekir
        self.assertGreater(len(heap.word_counts), 0)
    
    def test_read_empty_file(self):
        """Boş dosya testı"""
        test_file = os.path.join(self.temp_dir, "empty.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        heap = read_and_process_file(test_file)
        self.assertEqual(len(heap.word_counts), 0)
    
    def test_read_multiline_file(self):
        """Çok satırlı dosya testı"""
        test_file = os.path.join(self.temp_dir, "multiline.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Ankara\nKonya\nAnkara\nVan\nAnkara")
        
        heap = read_and_process_file(test_file)
        self.assertEqual(heap.word_counts["ankara"], 3)
        self.assertEqual(heap.word_counts["konya"], 1)
    
    def test_read_file_not_found(self):
        """Dosya bulunamadı testı"""
        with self.assertRaises(SystemExit):
            read_and_process_file("/nonexistent/file.txt")
    
    def test_file_with_whitespace(self):
        """Boşluk testı"""
        test_file = os.path.join(self.temp_dir, "whitespace.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("   Ankara   Konya   Ankara   ")
        
        heap = read_and_process_file(test_file)
        self.assertEqual(heap.word_counts["ankara"], 2)
    
    def test_file_with_tabs(self):
        """Tab karakterleri testı"""
        test_file = os.path.join(self.temp_dir, "tabs.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Ankara\t\tKonya\t\tAnkara")
        
        heap = read_and_process_file(test_file)
        self.assertEqual(heap.word_counts["ankara"], 2)


class TestIntegration(unittest.TestCase):
    """Entegrasyon testleri (bütün sistem)"""
    
    def setUp(self):
        """Test verileri hazırla"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Test dosyalarını sil"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Tam iş akışı testı"""
        # Dosya oluştur
        test_file = os.path.join(self.temp_dir, "workflow.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Adana Ankara Adana Ankara Adana Ankara Adana Konya Van")
        
        # Dosya oku ve işle
        heap = read_and_process_file(test_file)
        
        # Heap oluştur
        heap.build_heap()
        
        # Çıktı al
        output = heap.get_sorted_output()
        
        # Kontroller
        self.assertEqual(len(heap.word_counts), 4)  # 4 benzersiz kelime
        self.assertGreater(len(output), 0)
        
        # İlk kelime A harfi ile başlamalı
        self.assertEqual(output[0][0], 'A')
        
        # Adana en fazla geçmiş kelime olmalı
        self.assertEqual(output[0][1], "adana")
        self.assertEqual(output[0][2], 4)
    
    def test_sorting_order(self):
        """Sıralama düzeni testı"""
        test_file = os.path.join(self.temp_dir, "sorting.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Van Ankara Sivas Konya Adana")
        
        heap = read_and_process_file(test_file)
        heap.build_heap()
        output = heap.get_sorted_output()
        
        # Harflerin sırası: A < K < S < V (A 2 kez, diğerleri 1 kez)
        letters = [item[0] for item in output]
        self.assertEqual(sorted(set(letters)), ['A', 'K', 'S', 'V'])
    
    def test_large_file_performance(self):
        """Performans testı (büyük dosya)"""
        import time
        
        test_file = os.path.join(self.temp_dir, "large.txt")
        
        # 10000 kelime yaz
        with open(test_file, 'w', encoding='utf-8') as f:
            words = ["Ankara", "Konya", "Van", "Sivas", "Adana"] * 2000
            f.write(" ".join(words))
        
        # Zaman ölç
        start = time.time()
        heap = read_and_process_file(test_file)
        heap.build_heap()
        end = time.time()
        
        # 1 saniyede bitmeli
        self.assertLess(end - start, 1.0)


class TestEdgeCases(unittest.TestCase):
    """Uç durumlar testleri"""
    
    def setUp(self):
        self.heap = DualKeyHeap()
    
    def test_single_character_words(self):
        """Tek karakter kelimeler"""
        self.heap.add_word("a")
        self.heap.add_word("b")
        self.heap.add_word("a")
        
        self.assertEqual(self.heap.word_counts["a"], 2)
        self.assertEqual(self.heap.word_counts["b"], 1)
    
    def test_very_long_word(self):
        """Çok uzun kelime"""
        long_word = "a" * 1000
        self.heap.add_word(long_word)
        
        self.assertEqual(self.heap.word_counts[long_word], 1)
    
    def test_unicode_characters(self):
        """Unicode karakterler"""
        self.heap.add_word("Çankırı")
        self.heap.add_word("çankırı")
        
        # Küçük harfe dönüştürülecek
        self.assertGreater(len(self.heap.word_counts), 0)
    
    def test_mixed_case_consistency(self):
        """Karışık harf konsistansı"""
        variations = ["TEST", "Test", "test", "TeSt"]
        for word in variations:
            self.heap.add_word(word)
        
        self.assertEqual(self.heap.word_counts["test"], len(variations))


def run_tests():
    """Test'leri çalıştır"""
    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tüm test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestDualKeyHeap))
    suite.addTests(loader.loadTestsFromTestCase(TestFileProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Test'leri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Özet yazdır
    print("\n" + "="*70)
    print(f"Toplam Test: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hatalar: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    # Unittest'i çalıştır
    success = run_tests()
    sys.exit(0 if success else 1)
