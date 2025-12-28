export const metadata = { title: "GENISI", description: "Premium AI Orchestra" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body className="min-h-screen font-sans">{children}</body>
    </html>
  );
}
