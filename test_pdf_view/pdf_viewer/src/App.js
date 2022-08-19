import React, { useState } from 'react';
// import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import { Document } from 'react-pdf/dist/esm/entry.webpack';
import { Page } from 'react-pdf/dist/esm/entry.webpack';
import { pdfjs } from 'react-pdf/dist/esm/entry.webpack';


function App() {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  return (
    <div>
      <Document file="CI_DSA_study_guide.pdf" onLoadSuccess={onDocumentLoadSuccess}>
        <Page pageNumber={pageNumber} />
      </Document>
      <p>
        Page {pageNumber} of {numPages}
      </p>
    </div>
  );
}

export default App;
