/**
 * Info Modal Controller & Dynamic Sample Excel Downloader
 */

const sampleDataMap = {
  internal: {
    title: 'Internal Exam Marksheet Format',
    columns: ['Roll No', 'Marks'],
    allowedType: '.xlsx, .xls',
    sampleRows: [
      { 'Roll No': 1, 'Marks': 34 },
      { 'Roll No': 2, 'Marks': 27 },
      { 'Roll No': 3, 'Marks': 42 },
      { 'Roll No': 4, 'Marks': 18 }
    ],
    rules: [
      'The file must contain exactly two columns: "Roll No" and "Marks".',
      'Roll No must be unique (no duplicate student roll numbers allowed).',
      'Marks must be numeric values.',
      'Headers must match case-sensitively.'
    ]
  },
  external: {
    title: 'External Exam Marksheet Format',
    columns: ['Roll No', 'Marks'],
    allowedType: '.xlsx, .xls',
    sampleRows: [
      { 'Roll No': 1, 'Marks': 56 },
      { 'Roll No': 2, 'Marks': 61 },
      { 'Roll No': 3, 'Marks': 72 },
      { 'Roll No': 4, 'Marks': 49 }
    ],
    rules: [
      'The file must contain exactly two columns: "Roll No" and "Marks".',
      'Roll No must be unique.',
      'Marks must be numeric values.',
      'Internal and External marks must NEVER be merged in the same file.'
    ]
  },
  co: {
    title: 'Course Outcomes (CO) Format',
    columns: ['CO Number', 'Statement'],
    allowedType: '.xlsx, .xls',
    sampleRows: [
      { 'CO Number': 'CO1', 'Statement': 'Understand programming fundamentals' },
      { 'CO Number': 'CO2', 'Statement': 'Develop object oriented applications' },
      { 'CO Number': 'CO3', 'Statement': 'Design database applications' },
      { 'CO Number': 'CO4', 'Statement': 'Build web applications' }
    ],
    rules: [
      'File must contain columns: "CO Number" and "Statement".',
      'CO Number should be unique identifiers (CO1, CO2, etc.).',
      'Statement should be descriptive text explaining the learning outcome.'
    ]
  },
  po: {
    title: 'Program Outcomes (PO) Format',
    columns: ['PO Number', 'Statement'],
    allowedType: '.xlsx, .xls',
    sampleRows: [
      { 'PO Number': 'PO1', 'Statement': 'Engineering Knowledge' },
      { 'PO Number': 'PO2', 'Statement': 'Problem Analysis' },
      { 'PO Number': 'PO3', 'Statement': 'Modern Tool Usage' },
      { 'PO Number': 'PO4', 'Statement': 'Communication Skills' }
    ],
    rules: [
      'File must contain columns: "PO Number" and "Statement".',
      'PO Number should be unique identifiers (PO1, PO2, etc.).',
      'Both CO and PO sheets are mandatory for Module 2.'
    ]
  }
};

let currentModalType = null;

function initModal() {
  const modalBackdrop = document.getElementById('info-modal');
  const modalCloseBtn = document.getElementById('modal-close-btn');
  const modalOkBtn = document.getElementById('modal-ok-btn');
  const downloadSampleBtn = document.getElementById('modal-download-sample');

  document.querySelectorAll('.info-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const type = btn.getAttribute('data-info');
      openInfoModal(type);
    });
  });

  const closeModal = () => {
    modalBackdrop.classList.remove('open');
  };

  modalCloseBtn.addEventListener('click', closeModal);
  modalOkBtn.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });

  downloadSampleBtn.addEventListener('click', () => {
    if (currentModalType) {
      downloadSampleExcel(currentModalType);
    }
  });
}

function openInfoModal(type) {
  const info = sampleDataMap[type];
  if (!info) return;

  currentModalType = type;
  document.getElementById('modal-title').textContent = info.title;

  let html = `
    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.9rem; font-weight: 700; margin-bottom: 0.5rem;">Validation Rules</h4>
      <ul style="padding-left: 1.25rem; font-size: 0.85rem; color: var(--color-text-secondary);">
        ${info.rules.map(r => `<li style="margin-bottom: 0.25rem;">${r}</li>`).join('')}
      </ul>
    </div>

    <div style="margin-bottom: 1.25rem;">
      <h4 style="font-size: 0.9rem; font-weight: 700; margin-bottom: 0.5rem;">Expected Format & Sample Data</h4>
      <div class="table-responsive">
        <table class="table">
          <thead>
            <tr>
              ${info.columns.map(c => `<th>${c}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
            ${info.sampleRows.map(row => `
              <tr>
                ${info.columns.map(c => `<td>${row[c]}</td>`).join('')}
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;

  document.getElementById('modal-body').innerHTML = html;
  document.getElementById('info-modal').classList.add('open');
}

/**
 * Downloads sample Excel file directly from backend or fallback to CSV
 */
async function downloadSampleExcel(type) {
  const info = sampleDataMap[type];
  if (!info) return;

  try {
    const backendUrl = `http://127.0.0.1:8000/api/v1/templates/download/${type}`;
    const response = await fetch(backendUrl);
    
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `Sample_${type.toUpperCase()}_Template.xlsx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
      if (window.showToast) window.showToast(`Sample Excel template downloaded (.xlsx)`, 'success');
      return;
    }
  } catch (e) {
    // If backend endpoint is unreachable, fallback to CSV generator
  }

  // Fallback CSV generator
  const headers = info.columns.join(',');
  const rows = info.sampleRows.map(r => info.columns.map(c => `"${r[c]}"`).join(','));
  const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\n");

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `Sample_${type.toUpperCase()}_Template.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  if (window.showToast) {
    window.showToast(`Sample template downloaded (.csv)`, 'success');
  }
}

window.initModal = initModal;
