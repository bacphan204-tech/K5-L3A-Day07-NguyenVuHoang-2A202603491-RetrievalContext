"""Build/evidence-check the Day 7 benchmark without running any retriever/model."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from benchmark import pipeline_input, validate_cases, validate_minimums

DAY6 = ROOT.parent / "K5-L3A-Day06-NguyenVuHoang-2A202603491-DataIngestionEngineering"
SOURCE_ID = "openstax-principles-economics-3e"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def new_answer(cid, question, answer, page, evidence, topic):
    return {"id": cid, "split": "test", "question": question, "answerable": True,
            "expected_behavior": "search_and_answer", "expected_answer": answer,
            "gold": [{"source_id": SOURCE_ID, "page": page, "evidence": evidence}],
            "topic": topic, "filter": {}, "origin": "New Day 7 question, not a Day 6 test reuse",
            "review_status": "AI-authored source-text check; student confirmation pending"}


def absent(cid, split, question, reason, terms, inspection_pages, reasoning, pages):
    return {"id": cid, "split": split, "question": question, "answerable": False,
            "expected_behavior": "search_and_abstain", "absence_reason": reason, "filter": {},
            "absence_review": {"search_terms": terms,
                "term_page_hits": {term: [p["page"] for p in pages if term.casefold() in p["text"].casefold()] for term in terms},
                "scope": "All 52 indexed text pages; not a top-k retrieval result",
                "inspection_pages": inspection_pages, "reasoning": reasoning,
                "status": "AI initial text/scope review; student source confirmation pending"}}


def build():
    chunks = json.loads((ROOT / "data/day6/chunks.json").read_text(encoding="utf-8"))
    pages = json.loads((ROOT / "data/day6/pages.json").read_text(encoding="utf-8"))
    old_path = DAY6 / "benchmark/questions.jsonl"
    old = [json.loads(line) for line in old_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    dev, exclusions = [], []
    for q in old:
        if q["split"] != "dev":
            continue
        candidates = [{"source_id": q["gold_source_id"], "page": q["gold_page"], "evidence": q["evidence_quote"]}]
        candidates += [{"source_id": g["source_id"], "page": g["page"], "evidence": g["evidence_quote"]} for g in q.get("gold_alternatives", [])]
        gold = []
        for g in candidates:
            if any(c["source_id"] == g["source_id"] and c["page"] == g["page"] and g["evidence"] in c["text"] for c in chunks):
                gold.append(g)
            else:
                exclusions.append({"day6_id": q["id"], "page": g["page"], "reason": "Quote crosses B chunk boundary; excluded from single-chunk strict gold, not declared invalid source evidence"})
        case = {"id": "d7-dev-" + q["id"], "split": "dev", "question": q["question"],
                "answerable": True, "expected_behavior": "search_and_answer", "expected_answer": q["expected_answer"],
                "gold": gold, "filter": q["filter"], "origin": {"project": "Day 6", "question_id": q["id"], "split": "dev"},
                "review_status": "AI-authored source-text check; student confirmation pending"}
        if case["filter"]:
            case["filter_provenance"] = "Chapter explicitly stated in the question, not inferred from gold"
        if q["id"] == "q04":
            case["expected_answer"] = "Giá cân bằng 1,40 USD/gallon; lượng cân bằng 600 triệu gallon trong ví dụ."
        if q["id"] == "q06":
            case["expected_answer"] = "Giữ các yếu tố liên quan khác không đổi khi phân tích tác động của yếu tố đang xét."
        dev.append(case)
    dev += [
        absent("d7-dev-u01", "dev", "Theo bộ tài liệu này, mức lương tối thiểu vùng I của Việt Nam năm 2026 chính xác là bao nhiêu đồng/tháng?",
               "Corpus không cung cấp quy định lương tối thiểu vùng I Việt Nam năm 2026.",
               ["Vietnam", "Viet Nam", "2026", "minimum wage"], [28, 42, 43],
               "Các trang về lương tối thiểu/living wage trình bày ví dụ Hoa Kỳ và mô hình, không có bảng mức lương theo vùng Việt Nam hay căn cứ năm 2026. Không dùng ví dụ USD/giờ thay cho số đồng/tháng được hỏi.", pages),
        absent("d7-dev-u02", "dev", "Theo tài liệu, hệ số co giãn cầu theo giá của xăng tại Việt Nam năm 2025 chính xác bằng bao nhiêu?",
               "Ví dụ xăng không cung cấp ước lượng co giãn thực nghiệm cho Việt Nam năm 2025.",
               ["Vietnam", "Viet Nam", "2025", "elasticity", "gasoline"], [4, 5, 8, 9],
               "Có bảng giá/lượng giả định và ví dụ cân bằng xăng; không có dữ liệu hoặc ước lượng cho địa điểm, năm được hỏi. Không tự biến phép tính từ bảng minh họa thành hệ số thực nghiệm Việt Nam.", pages)
    ]
    test = [
        new_answer("d7-test-q01", "Trong ví dụ máy tính bảng, một người sẵn sàng trả 90 USD nhưng thực trả 80 USD nhận được bao nhiêu thặng dư tiêu dùng? Giải thích phép tính.",
                   "Thặng dư tiêu dùng là 10 USD cho chiếc máy tính bảng: 90 - 80 = 10 USD.", 29,
                   "Those consumers who would have been willing to pay $90 for a tablet based on the utility they expect to receive from it, but who were able to pay the equilibrium price of $80, clearly received a benefit beyond what they had to pay. Remember, the demand curve traces consumers’ willingness to pay for different quantities. The amount that individuals would have been willing to pay, minus the amount that they actually paid, is called consumer surplus.", "consumer_surplus_calculation"),
        new_answer("d7-test-q02", "Chính phủ thường hỗ trợ giá nông sản bằng cách tham gia thị trường như thế nào, và việc đó tác động ra sao đến cầu và giá?",
                   "Chính phủ mua sản phẩm trên thị trường, làm tăng cầu để giữ giá cao hơn mức giá nếu không có biện pháp này.", 28,
                   "The most common way price supports work is that the government enters the market and buys up the product, adding to demand to keep prices higher than they otherwise would be.", "agricultural_price_support"),
        new_answer("d7-test-q03", "Trong ví dụ thị trường tín dụng thẻ, ở lãi suất 13% lượng vốn được cầu và được cung là bao nhiêu? Thị trường thiếu hay dư bao nhiêu tỷ USD?",
                   "Lượng cầu 700 tỷ USD, lượng cung 510 tỷ USD; thiếu vốn 190 tỷ USD, vì 700 - 510 = 190.", 46,
                   "If the interest rate is below the equilibrium, then excess demand or a shortage of funds occurs in this market. At an interest rate of 13%, the quantity of funds credit card borrowers demand increases to $700 billion, but the quantity credit card firms are willing to supply is only $510 billion.", "credit_shortage_calculation"),
        new_answer("d7-test-q04", "Khi người tiêu dùng và doanh nghiệp tin tưởng hơn rằng họ có thể trả nợ trong tương lai, cầu vốn tài chính tại một mức lãi suất cho trước dịch chuyển thế nào?",
                   "Cầu vốn tài chính tăng tại mỗi mức lãi suất cho trước; đường cầu dịch sang phải.", 47,
                   "Thus, when consumers and businesses have greater confidence that they will be able to repay in the future, the quantity demanded of financial capital at any given interest rate will shift to the right.", "repayment_confidence"),
        new_answer("d7-test-q05", "Nếu khoản đầu tư A trở nên rủi ro hơn trong khi B là lựa chọn thay thế, người tiết kiệm chuyển vốn ra sao và đường cung vốn cho A, B dịch chuyển hướng nào?",
                   "Người tiết kiệm chuyển vốn từ A sang B; cung vốn cho A dịch trái, cung vốn cho B dịch phải.", 47,
                   "If Investment A becomes more risky, or the return diminishes, then savers will shift their funds to Investment B—and the supply curve of financial capital for Investment A will shift back to the left while the supply curve of capital for Investment B shifts to the right.", "investment_risk_reallocation"),
        absent("d7-test-u01", "test", "Theo bộ tài liệu này, lãi suất cho vay mua nhà cụ thể của Vietcombank trong tháng 11/2026 là bao nhiêu phần trăm mỗi năm?",
               "Corpus không có biểu lãi suất sản phẩm vay mua nhà của Vietcombank tháng 11/2026.",
               ["Vietcombank", "2026", "mortgage"], [44, 45, 46, 49, 50],
               "Chương thị trường tài chính mô tả mô hình và ví dụ tín dụng; việc nhắc đến khoản vay nhà hoặc đường link FRED không cung cấp báo giá của ngân hàng Việt Nam, sản phẩm và tháng được hỏi. Phạm vi chỉ là corpus, không truy cập nguồn ngoài.", pages),
        absent("d7-test-u02", "test", "Dựa riêng vào tài liệu, giá cân bằng xăng tại Hà Nội ngày 14/11/2026 chính xác là bao nhiêu đồng/lít?",
               "Corpus không cung cấp giá xăng thực tế hoặc hàm cung cầu cho Hà Nội tại ngày được hỏi.",
               ["Hanoi", "Ha Noi", "2026", "gasoline"], [4, 5, 8, 9],
               "Ví dụ xăng dùng USD/gallon và triệu gallon, không phải dữ liệu Hà Nội theo ngày. Không chuyển ví dụ cân bằng trong sách thành báo giá hiện hành hoặc tự quy đổi sang đồng/lít khi thiếu dữ liệu.", pages)
    ]
    report = validate_cases(dev + test, chunks)
    validate_minimums(report["counts"])
    folder = ROOT / "benchmark"
    # Avoid silently overwriting a benchmark once a later experiment freezes it.
    if (folder / "frozen.json").exists() or (ROOT / "results/experiment_lock.json").exists():
        raise RuntimeError("Benchmark is frozen; preserve the old experiment before creating a new benchmark")
    for split, cases in (("dev", dev), ("test", test)):
        write(folder / f"{split}.json", cases)
        write(folder / f"{split}.inputs.json", [pipeline_input(c) for c in cases])
    manifest = {"version": 1, "counts": report["counts"], "gold_semantics": "Each gold item is a complete alternative; one valid item suffices. No multi-hop gold in this version.",
                "source_id": SOURCE_ID, "corpus_sha256": digest(ROOT / "data/day6/chunks.json"),
                "day6_benchmark_sha256": digest(old_path), "reused_day6_dev_ids": [q["id"] for q in old if q["split"] == "dev"],
                "day6_test_reused": False, "excluded_day6_alternatives": exclusions,
                "question_files_sha256": {f"{s}.json": digest(folder / f"{s}.json") for s in ("dev", "test")},
                "test_policy": "New AI-authored test; held out from retrieval/configuration selection. Authoring/structural evidence checks are not model evaluation. The author has seen test labels, so this is not an external blind evaluation.",
                "review_status": "Draft benchmark: student source/absence confirmation pending",
                "benchmark_run": False, "student_confirmed": False,
                "license": "OpenStax Principles of Economics 3e excerpts/evidence: CC BY-NC-SA 4.0; retain source attribution"}
    write(folder / "manifest.json", manifest)
    write(ROOT / "results/part04/validation.json", {"status": "passed", **report,
          "review_status": manifest["review_status"], "note": "Structural/quote checks only; not retrieval or LLM quality metrics"})
    print(json.dumps({"status": "PASS", "counts": report["counts"], "answerable_total": sum(c["answerable"] for c in dev+test),
                      "unanswerable_total": sum(not c["answerable"] for c in dev+test),
                      "benchmark_run": False, "student_confirmed": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="Validate existing benchmark without rewriting it or printing test answers")
    args = parser.parse_args()
    if args.check_only:
        folder = ROOT / "benchmark"
        chunks_path = ROOT / "data/day6/chunks.json"
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        all_cases = []
        for split in ("dev", "test"):
            path = folder / f"{split}.json"
            if digest(path) != manifest["question_files_sha256"][path.name]:
                raise ValueError(f"{split} benchmark changed since manifest was written")
            cases = json.loads(path.read_text(encoding="utf-8"))
            if any(c["split"] != split for c in cases):
                raise ValueError("Case is stored in the wrong split file")
            inputs = json.loads((folder / f"{split}.inputs.json").read_text(encoding="utf-8"))
            if inputs != [pipeline_input(c) for c in cases]:
                raise ValueError(f"{split}: pipeline inputs differ or contain evaluator labels")
            all_cases.extend(cases)
        if digest(chunks_path) != manifest["corpus_sha256"]:
            raise ValueError("Corpus changed since benchmark authoring")
        checked = validate_cases(all_cases, json.loads(chunks_path.read_text(encoding="utf-8")))
        validate_minimums(checked["counts"])
        print(json.dumps({"status": "PASS", "counts": checked["counts"], "gold_resolves": True,
                          "pipeline_inputs_have_no_labels": True, "benchmark_run": False,
                          "student_confirmed": manifest["student_confirmed"]}, indent=2))
    else:
        build()
