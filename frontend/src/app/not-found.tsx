import Link from "next/link";
export default function NotFound() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-wellness-pale to-white flex items-center justify-center">
      <div className="text-center max-w-md mx-auto px-4">
        <div className="w-20 h-20 bg-wellness-green rounded-2xl flex items-center justify-center mx-auto mb-6"><span className="text-white font-bold text-2xl">404</span></div>
        <h1 className="text-3xl font-bold text-wellness-dark mb-3">Page Not Found</h1>
        <p className="text-gray-600 mb-8">The page you are looking for does not exist or has been moved.</p>
        <Link href="/" className="bg-wellness-green text-white px-8 py-3 rounded-xl font-bold hover:bg-wellness-dark transition-all">Back to Home</Link>
      </div>
    </div>
  );
}