from unittest.mock import patch
import cli

def test_view_all(capsys):
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': '1', 'name': 'Apple', 'price': 1.99, 'stock_quantity': 10}]
        cli.view_all()
        captured = capsys.readouterr()
        assert 'Apple' in captured.out
        assert '1.99' in captured.out

def test_add_item(monkeypatch, capsys):
    inputs = iter(['Orange', '2.50', '15', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('requests.post') as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'abc', 'name': 'Orange', 'price': 2.5, 'stock_quantity': 15}
        cli.add_item()
        captured = capsys.readouterr()
        assert 'Item added successfully' in captured.out
        assert 'Orange' in captured.out