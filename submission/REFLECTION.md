# Day 23 Lab Reflection

> Fill in each section. Grader reads the "What I'd change" paragraph closest.

**Student:** _Đỗ Trung Đức_
**Submission date:** _2026-06-29_
**Lab repo URL:** _https://github.com/DoTrungDuc1908/Day23-Track2-Observability-Lab_

---

## 1. Hardware + setup output

Paste output of `python3 00-setup/verify-docker.py`:

```json
{
  "docker": {
    "ok": true,
    "version": "27.5.1"
  },
  "compose_v2": {
    "ok": true,
    "version": "2.32.4-desktop.1"
  },
  "ram_gb_available": 5.72,
  "ram_ok": true,
  "required_ports": [
    8000,
    9090,
    9093,
    3000,
    3100,
    16686,
    4317,
    4318,
    8888
  ],
  "bound_ports": [],
  "all_ports_free": true
}
```

---

## 2. Track 02 — Dashboards & Alerts

### 6 essential panels (screenshot)

Drop `submission/screenshots/dashboard-overview.png`.

### Burn-rate panel

Drop `submission/screenshots/slo-burn-rate.png`.

### Alert fire + resolve

| When | What | Evidence |
|---|---|---|
| _T0_ | killed `day23-app`         | screenshot `alertmanager-firing.png` |
| _T0+90s_ | `ServiceDown` fired   | screenshot `slack-firing.png` |
| _T1_ | restored app              | — |
| _T1+60s_ | alert resolved        | screenshot `slack-resolved.png` |

### One thing surprised me about Prometheus / Grafana

Một điểm thú vị là Prometheus hỗ trợ PromQL có thể kết hợp nhiều metric với nhau để tính toán được SLO Burn Rate một cách rất hiệu quả (Ví dụ tính toán rate lỗi chia cho rate tổng để ra error budget). Ngoài ra Grafana có thể render biểu đồ rất đẹp và lấy dữ liệu trực tiếp từ Prometheus mà không cần thêm middleware.

---

## 3. Track 03 — Tracing & Logs

### One trace screenshot from Jaeger

Drop `submission/screenshots/jaeger-trace.png` showing `embed-text → vector-search → generate-tokens` spans.

### Log line correlated to trace

Paste the log line and the trace_id it links to:

```json
{"model": "llama3-mock", "input_tokens": 4, "output_tokens": 54, "quality": 0.82, "duration_seconds": 0.1539, 
"trace_id": "618ead29419661d43f60eeed53342eff", "event": "prediction served", "level": "info", "timestamp": 
"2026-06-29T03:24:23.765884Z"}
```

### Tail-sampling math

Gọi E là tỉ lệ request bị lỗi (Errors), S là tỉ lệ request chạy chậm (Slow >2s).
Chính sách tail-sampling giữ lại 100% Errors, 100% Slow và 1% các request bình thường (probabilistic).
Do đó, với N traces/sec, số lượng trace được giữ lại (fraction kept) sẽ xấp xỉ: 
N * (E + S + 0.01 * (1 - E - S))

---

## 4. Track 04 — Drift Detection

### PSI scores

Paste `04-drift-detection/reports/drift-summary.json`:

```json
{
  "prompt_length": {
    "PSI": 3.461234978939223,
    "KL": 1.7984852928823521,
    "KS": 0.7022879301648489,
    "drift": "yes"
  },
  "embedding_norm": {
    "PSI": 0.019488806202422204,
    "KL": 0.03158933227915501,
    "KS": 0.05191147055743154,
    "drift": "no"
  },
  "response_length": {
    "PSI": 0.015949506692257218,
    "KL": 0.01825126831006509,
    "KS": 0.05586616452179836,
    "drift": "no"
  },
  "response_quality": {
    "PSI": 8.848813735166412,
    "KL": 13.501227091533033,
    "KS": 0.941,
    "drift": "yes"
  }
}
```

### Which test fits which feature?

- **prompt_length**: Dùng KS (Kolmogorov-Smirnov) vì đây là phân phối liên tục của chiều dài (hoặc nếu chia bin thì dùng PSI). 
- **embedding_norm**: MMD (Maximum Mean Discrepancy) hoặc KS để phát hiện sự thay đổi trên không gian vector.
- **response_length**: KS hoặc PSI tương tự như prompt_length.
- **response_quality**: PSI hoặc KL Divergence vì là phân phối có thể có các đặc tính categorical/binned rõ ràng. PSI thường rất phổ biến trong tài chính và đánh giá model drift.

---

## 5. Track 05 — Cross-Day Integration

### Which prior-day metric was hardest to expose? Why?

Tích hợp metric từ một Vector Store giả lập (Day 19) đòi hỏi phải dựng một stub HTTP server trả về prometheus metric. Khó nhất là làm sao cấu hình Prometheus (`prometheus.yml`) để cào (scrape) đúng địa chỉ `host.docker.internal` trên Windows thay vì IP nội bộ của docker-compose, nhằm hiển thị lên Grafana.

---

## 6. The single change that mattered most

Điều quan trọng nhất làm cho hệ thống từ "hoạt động" (works) trở thành "hữu ích" (useful) chính là **cơ chế Tail-Sampling dựa trên điều kiện (Status / Latency) thay vì Head-Sampling ngẫu nhiên**.

Thay vì chỉ lấy mẫu ngẫu nhiên (Head-sampling) từ đầu khiến ta dễ dàng bỏ lỡ những request bị lỗi hoặc xử lý chậm (chỉ chiếm thiểu số, ví dụ 1% của hàng triệu request), việc áp dụng Tail-Sampling (gom toàn bộ span lại rồi quyết định ở đoạn cuối) đảm bảo 100% các request lỗi (ERROR) và request chậm (>2000ms) được giữ lại, đồng thời chỉ lấy 1% request bình thường. Điều này liên kết trực tiếp với khái niệm "Tối ưu chi phí lưu trữ nhưng không mất dữ liệu quan trọng" trong bài học: ta có thể phân tích cặn kẽ mọi lỗi mà không bị quá tải bộ nhớ hệ thống tracing.
