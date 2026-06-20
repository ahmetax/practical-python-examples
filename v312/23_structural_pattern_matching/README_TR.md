# Proje 23: Yapısal Pattern Matching (match-case)

Python 3.10+ ile tanıtılan yapısal pattern matching (`match-case`) özelliğini nasıl uygulayacağını gösteren, temiz, üretim ortamına hazır bir örnektir. Bu pattern, karmaşık gelen payload'ları, veri tiplerini ve yapısal koşulları doğrularken iç içe geçmiş `if-elif-else` dallarına okunaklı, ifade gücü yüksek bir alternatif sağlar.

## Mimari Hedef
Uygulama, bir e-ticaret backend'i için bir komut işleme mimarisini modellemektedir. Çeşitli veri şekillerindeki (düz dizeler, yapılandırılmış diziler/listeler, tipli veri nesneleri ve sözlük eşlemeleri) gelen sistem payload'larını ayrıştırır ve girdi formatlarını dinamik olarak doğrulamak için yürütme guard'ları (execution guards) uygular.

## Bu Projeyi Sıfırdan Nasıl Oluşturulur

### Adım 1: Dizin Kurulumu
Çalışma alanınızda projeniz için yeni bir klasör oluşturun:
```bash
mkdir 23_structural_pattern_matching
cd 23_structural_pattern_matching

### Step 2: Establish the Core Implementation
Create a single python file named main.py. Inside this script, structure your logic step-by-step using standard libraries:

Define Data Objects: Import dataclass from dataclasses. Implement an Order object with parameters representing product identity (product_name), amounts (quantity), and current tracking state (status).

Build the Dispatcher: Define a central routing function (e.g., process_command(command)) that accepts a generic input parameter.

Draft the Match Patterns:

Literal Pattern: Check for simple command strings like "EXIT" to trigger system shutdowns.

Sequence Pattern: Capture explicit operations passed as a list (e.g., ["add", item, qty]), extracting the index variables only if they conform to specific type assertions like str and int.

Guard Expressions: Match slice elements (e.g., a deletion instruction ["delete", *ids]) and apply a hard filter condition using the if statement to ensure the identifier array is not empty.

Object Pattern: Inspect your instance signatures. Isolate an object like Order matching specific interior flag attributes (status="shipped"). Use standard binding (as order) to fall back gracefully on general object routing.

Mapping Pattern: Extract keyed payloads via dictionary matchers (e.g., checks looking for {"type": "invoice", "amount": float}).

Wildcard: Conclude with a catch-all block (case _:) to report malformed, unhandled actions safely.

### Step 3: Run and Verify
Add a standard conditional driver script (if __name__ == "__main__":) to queue a heterogeneous array of input variants—including correct schemas, edge cases, object types, and completely invalid data shapes—and iterate through them. Execute the script natively:

```bash
python main.py


---